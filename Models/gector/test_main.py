import os
from typing import Dict, List

import torch
from gector import GECToR, load_verb_dict, predict, predict_verbose
from transformers import AutoTokenizer


def visualizer(iteration_log: List[List[Dict]]):
    # Generate a string to visualize the predictions.
    strs = ""
    for sent_id, sent in enumerate(iteration_log):
        strs += f"=== Line {sent_id} ===\n"
        for itr_id, itr in enumerate(sent):
            if itr["tag"] is None:
                strs += " ".join(itr["src"]).replace("$START", "").strip() + "\n"
                break
            strs += f"== Iteration {itr_id} ==\n"
            src_str = "|"
            tag_str = "|"
            for tok, tag in zip(itr["src"], itr["tag"]):
                max_len = max(len(tok), len(tag)) + 1
                src_str += tok + " " * (max_len - len(tok)) + "|"
                tag_str += tag + " " * (max_len - len(tag)) + "|"
            strs += src_str + "\n"
            strs += tag_str + "\n"
        strs += "\n"
    return strs


def main():
    print("시작 ~ ^^")
    gector_path = "/home/dashic/gector-test/gector-test/gector"

    model_path = "gotutiyan/gector-roberta-large-5k"
    input_path = os.path.join(gector_path, "input", "hbcominatya.txt")
    verb_path = os.path.join(gector_path, "data", "verb-form-vocab.txt")
    visualize = os.path.join(gector_path, "viz_output", "hbcominatya_rob.txt")
    out = os.path.join(gector_path, "viz_output", "out.txt")

    keep_confidence = 0.0
    min_error_prob = 0.0
    batch_size = 128
    n_iteration = 5

    model = GECToR.from_pretrained(model_path).eval()
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    srcs = open(input_path).read().rstrip().split("\n")
    encode, decode = load_verb_dict(verb_path)
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
    if visualize is not None:
        final_corrected_sents, iteration_log = predict_verbose(**predict_args)
        strs = visualizer(iteration_log)
        with open(visualize, "w") as fp:
            fp.write(strs)
    else:
        final_corrected_sents = predict(**predict_args)
    with open(out, "w") as f:
        f.write("\n".join(final_corrected_sents))

    print(f"=== Finished ===")


if __name__ == "__main__":
    main()
