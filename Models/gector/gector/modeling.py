import json
import os
from dataclasses import dataclass
from typing import List, Optional, Tuple, Union

import torch
import torch.nn as nn
import torch.nn.functional as F
from huggingface_hub import ModelCard, snapshot_download
from torch.nn import CrossEntropyLoss
from transformers import AutoConfig, AutoModel, AutoTokenizer, PreTrainedModel

from .configuration import GECToRConfig


@dataclass
class GECToROutput:
    loss: torch.Tensor = None
    loss_d: torch.Tensor = None
    loss_labels: torch.Tensor = None
    logits_d: torch.Tensor = None
    logits_labels: torch.Tensor = None
    accuracy: torch.Tensor = None
    accuracy_d: torch.Tensor = None


@dataclass
class GECToRPredictionOutput:
    probability_labels: torch.Tensor = None
    probability_d: torch.Tensor = None
    pred_labels: List[List[str]] = None
    pred_label_ids: torch.Tensor = None
    max_error_probability: torch.Tensor = None


class GECToR(PreTrainedModel):
    config_class = GECToRConfig

    def __init__(self, config: GECToRConfig):
        super().__init__(config)
        self.config = config
        self.tokenizer = AutoTokenizer.from_pretrained(self.config.model_id)
        if self.config.has_add_pooling_layer:
            self.bert = AutoModel.from_pretrained(
                self.config.model_id, add_pooling_layer=False
            )
        else:
            self.bert = AutoModel.from_pretrained(self.config.model_id)
        # +1 is for $START token
        self.bert.resize_token_embeddings(self.bert.config.vocab_size + 1)
        self.label_proj_layer = nn.Linear(
            self.bert.config.hidden_size, self.config.num_labels - 1
        )  # -1 is for <PAD>
        self.d_proj_layer = nn.Linear(
            self.bert.config.hidden_size, self.config.d_num_labels - 1
        )
        self.dropout = nn.Dropout(self.config.p_dropout)
        self.loss_fn = CrossEntropyLoss(label_smoothing=self.config.label_smoothing)

        self.post_init()
        self.tune_bert(False)

    def init_weight(self) -> None:
        self._init_weights(self.label_proj_layer)
        self._init_weights(self.d_proj_layer)

    def _init_weights(self, module) -> None:
        """Initialize the weights"""
        if isinstance(module, nn.Linear):
            # Slightly different from the TF version which uses truncated_normal for initialization
            # cf https://github.com/pytorch/pytorch/pull/5617
            module.weight.data.normal_(mean=0.0, std=self.config.initializer_range)
            if module.bias is not None:
                module.bias.data.zero_()
        return

    def tune_bert(self, tune=True):
        # If tune=False, only classifier layers will be tuned.
        for param in self.bert.parameters():
            param.requires_grad = tune
        return

    def forward(
        self,
        input_ids: Optional[torch.Tensor] = None,
        attention_mask: Optional[torch.Tensor] = None,
        token_type_ids: Optional[torch.Tensor] = None,
        position_ids: Optional[torch.Tensor] = None,
        inputs_embeds: Optional[torch.Tensor] = None,
        labels: Optional[torch.Tensor] = None,
        d_labels: Optional[torch.Tensor] = None,
        output_attentions: Optional[bool] = None,
        output_hidden_states: Optional[bool] = None,
        return_dict: Optional[bool] = None,
        word_masks: Optional[torch.Tensor] = None,
    ) -> GECToROutput:
        bert_logits = self.bert(
            input_ids,
            attention_mask=attention_mask,
            token_type_ids=token_type_ids,
            position_ids=position_ids,
            inputs_embeds=inputs_embeds,
            output_attentions=output_attentions,
            output_hidden_states=output_hidden_states,
            return_dict=return_dict,
        ).last_hidden_state
        logits_d = self.d_proj_layer(bert_logits)
        logits_labels = self.label_proj_layer(self.dropout(bert_logits))
        loss_d, loss_labels, loss = None, None, None
        accuracy, accuracy_d = None, None
        if d_labels is not None and labels is not None:
            pad_id = self.config.label2id[self.config.label_pad_token]
            # -100 is the default ignore_idx of CrossEntropyLoss
            labels[labels == pad_id] = -100
            d_labels[labels == -100] = -100
            loss_d = self.loss_fn(
                logits_d.view(-1, self.config.d_num_labels - 1),  # -1 for <PAD>
                d_labels.view(-1),
            )
            loss_labels = self.loss_fn(
                logits_labels.view(-1, self.config.num_labels - 1), labels.view(-1)
            )
            loss = loss_d + loss_labels

            pred_labels = torch.argmax(logits_labels, dim=-1)
            accuracy = torch.sum((labels == pred_labels) * word_masks) / torch.sum(
                word_masks
            )
            pred_d = torch.argmax(logits_d, dim=-1)
            accuracy_d = torch.sum((d_labels == pred_d) * word_masks) / torch.sum(
                word_masks
            )

        return GECToROutput(
            loss=loss,
            loss_d=loss_d,
            loss_labels=loss_labels,
            logits_d=logits_d,
            logits_labels=logits_labels,
            accuracy=accuracy,
            accuracy_d=accuracy_d,
        )

    def predict(
        self,
        input_ids: torch.Tensor,
        attention_mask: torch.Tensor,
        word_masks: torch.Tensor,
        keep_confidence: float = 0,
        min_error_prob: float = 0,
    ):
        with torch.no_grad():
            outputs = self.forward(input_ids, attention_mask)
            probability_labels = F.softmax(outputs.logits_labels, dim=-1)
            probability_d = F.softmax(outputs.logits_d, dim=-1)

            # Get actual labels considering inference parameters.
            keep_index = self.config.label2id[self.config.keep_label]
            probability_labels[:, :, keep_index] += keep_confidence
            incor_idx = self.config.d_label2id[self.config.incorrect_label]
            probability_d = probability_d[:, :, incor_idx]
            max_error_probability = torch.max(probability_d * word_masks, dim=-1)[0]
            probability_labels[
                max_error_probability < min_error_prob, :, keep_index
            ] = float("inf")
            pred_label_ids = torch.argmax(probability_labels, dim=-1)

            def convert_ids_to_labels(ids, id2label):
                labels = []
                for id in ids.tolist():
                    labels.append(id2label[id])
                return labels

            pred_labels = []
            for ids in pred_label_ids:
                labels = convert_ids_to_labels(ids, self.config.id2label)
                pred_labels.append(labels)

        return GECToRPredictionOutput(
            probability_labels=probability_labels,
            probability_d=probability_d,
            pred_labels=pred_labels,
            pred_label_ids=pred_label_ids,
            max_error_probability=max_error_probability,
        )
