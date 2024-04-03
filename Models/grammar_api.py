import json
import os

import nltk
import torch
import uvicorn
from fastapi import FastAPI, Form
from gector.gector import GECToR, load_verb_dict, predict_verbose
from nltk.tokenize import sent_tokenize
from transformers import AutoTokenizer
from typing_extensions import Annotated
from utils import gram_metrics, gram_out_json, gram_visualizer_json

app = FastAPI()
# FOAM 관련 참고
# @app.post("/files/")
# async def create_file(
#     fileb: Annotated[UploadFile, File()],
#     token: Annotated[str, Form()],
# ):
#     return {
#         "token": token,
#         "fileb_content_type": fileb.content_type,
#     }

model_path = "gotutiyan/gector-roberta-large-5k"
# input_path = os.path.join(gector_path, "input", "macominatya.json")

model = GECToR.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)
model.eval()


@app.post("/upload/")
async def upload_json(
    text: Annotated[str, Form()],
):
    try:

        gector_path = "./gector"
        verb_path = "./gector/data/verb-form-vocab.txt"

        # nltk.download("punkt")
        # print(text)
        # srcs = sent_tokenize(text)
        srcs = gram_visualizer_json.process_input_text(text)
        encode, decode = load_verb_dict(verb_path)

        transcription = text
        # parameter initialization
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

        # Grammar Error Correction Process
        final_corrected_sents, iteration_log = predict_verbose(**predict_args)
        checker_data = gram_visualizer_json.visualizer_json(
            iteration_log, final_corrected_sents
        )

        # dump visualized checker .json file
        check = os.path.join(gector_path, "check", "checker_data.json")

        with open(check, "w", encoding="utf-8") as c:
            json.dump(checker_data, c, indent="\t")

        # Run this part if you want the metric json file
        # metric = os.path.join(gector_path, "metric", "metric.json")
        # with open(metric, "w", encoding="utf-8") as r:
        #     json.dump(metric_data, r, indent="\t")

        # Final output
        phase = "phase_2"  # either "phase_1" or "phase_2"
        score_type = "pwc"  # "ec" or "psc" or "pwc"
        out_path = os.path.join(gector_path, "real", f"grammar_{phase}.json")
        score = gram_metrics.get_score(checker_data=checker_data, score_type=score_type)
        print(
            gram_out_json.create_json(
                phase=phase, out_path=out_path, score=score, check_data=checker_data
            )
        )

        return gram_out_json.create_json(
            phase=phase, out_path=out_path, score=score, check_data=checker_data
        )

    except Exception as e:
        return {"text": None, "status": f"Error: {str(e)}"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8888)
