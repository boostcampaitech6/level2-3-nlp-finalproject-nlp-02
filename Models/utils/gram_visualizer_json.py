import json
import os
from pprint import pprint
from typing import Dict, List

import torch
from gector.gector import GECToR, load_verb_dict, predict_verbose
from transformers import AutoTokenizer


def process_input_text(input_text: str):
    punctuation_marks = {'.', '!', '?'}

    sentences = []
    start = 0

    for i, char in enumerate(input_text):
        if char in punctuation_marks:
            sentence = input_text[start:i+1].strip()
            if sentence:
                sentences.append(sentence)
            start = i + 1

    if start < len(input_text):
        sentences.append(input_text[start:].strip())

    return sentences


def visualizer_json(iteration_log: List[List[Dict]], out_sentence):
    # Generate a string to visualize the predictions.
    outer_data = {}
    for sent_idx, sent in enumerate(iteration_log):
        og_sentence = " ".join([str(item) for item in sent[0]["src"][1:]])
        inner_data = {
            "edited": False,
            "sentence_list": [],
            "tag_list": [],
            "fin_sentence": "",
        }
        for _, itr in enumerate(sent):
            if itr["tag"] is None:
                break
            src_list = []
            tag_list = []
            for tok, tag in zip(itr["src"], itr["tag"]):
                # Append sentence:tag dictionary to the value of sent_dict for metric calculation
                src_list.append(tok)
                tag_list.append(tag)
            # adding src_list and tag_list to the inner dictionary
            inner_data["sentence_list"].append(src_list)
            inner_data["tag_list"].append(tag_list)
            inner_data["edited"] = True
        inner_data["fin_sentence"] = out_sentence[sent_idx]
        outer_data[og_sentence] = inner_data

    return outer_data


if __name__ == "__main__":
    gector_path = "../gector"

    with open(
        os.path.join(gector_path, "input", "macominatya.txt"), "r", encoding="utf-8"
    ) as file:
        sents = file.readlines()

    text_data = {"text": sents}
    with open(
        os.path.join(gector_path, "input", "macominatya.json"), "w", encoding="utf-8"
    ) as jf:
        json.dump(text_data, jf, indent="\t")

    # path initialization
    model_path = "gotutiyan/gector-roberta-large-5k"
    input_path = os.path.join(gector_path, "input", "macominatya.json")
    verb_path = os.path.join(gector_path, "data", "verb-form-vocab.txt")
    check = os.path.join(gector_path, "check", "final_check_ma.json")

    model = GECToR.from_pretrained(model_path).eval()
    tokenizer = AutoTokenizer.from_pretrained(model_path)

    # get all sentences
    with open(
        os.path.join(gector_path, "input", "macominatya.json"), "r", encoding="utf-8"
    ) as jf:
        data = json.load(jf)
        srcs = list(map(lambda x: x.strip(), data["text"]))
    encode, decode = load_verb_dict(verb_path)

    keep_confidence = 0.0
    min_error_prob = 0.0
    batch_size = 128
    n_iteration = 5

    if torch.cuda.is_available():
        model.cuda()

    predict_args = {
        "model": model,
        "tokenizer": tokenizer,
        "srcs": srcs,
        "encode": encode,
        "decode": decode,
        "keep_confidence": keep_confidence,
        "min_error_prob": min_error_prob,
        "batch_size": batch_size,
        "n_iteration": n_iteration,
    }

    final_corrected_sents, iteration_log = predict_verbose(**predict_args)
    json_data = visualizer_json(iteration_log, final_corrected_sents)

    # dump checker json file for metric calculation
    with open(check, "w", encoding="utf-8") as c:
        json.dump(json_data, c, indent="\t")

    print(f"=== Visualizer JSON Created ===")
