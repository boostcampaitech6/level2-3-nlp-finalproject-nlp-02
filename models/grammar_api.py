from fastapi import FastAPI, File, UploadFile, Body, HTTPException, Form
from typing import List
import torch
import uvicorn
import shutil
from pydantic import BaseModel
from typing_extensions import Annotated
import os
from logging import Logger
import uvicorn

from typing import Optional, Union, List, Pattern
from typing_extensions import Literal
import torch
import os
import torch
import json

from transformers import AutoTokenizer

from gector.gector import (
    GECToR,
    load_verb_dict,
    predict_verbose
)

from utils import gram_visualizer_json
from utils import gram_out_json
import nltk
from nltk.tokenize import sent_tokenize
import json

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
#input_path = os.path.join(gector_path, "input", "macominatya.json")

model = GECToR.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)
model.eval()

@app.post("/upload/")
async def upload_json(
    text: Annotated[str, Form()],
):
    try:
        
        gector_path = "/home/dashic/gector-test/gector-test/gector"
        verb_path = os.path.join(gector_path, "data", "verb-form-vocab.txt")
        

        nltk.download('punkt')
        print(text)
        srcs = sent_tokenize(text)
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
            'model': model,
            'tokenizer': tokenizer,
            'srcs': srcs,
            'encode': encode,
            'decode': decode,
            'keep_confidence': keep_confidence,
            'min_error_prob': min_error_prob,
            'batch_size': batch_size,
            'n_iteration': n_iteration
        }

        # Grammar Error Correction Process
        final_corrected_sents, iteration_log = predict_verbose(
            **predict_args
        )
        checker_data = gram_visualizer_json.visualizer_json(iteration_log, final_corrected_sents)

        # dump visualized checker .json file
        check = os.path.join(gector_path, "check", "final_check_ma.json")

        with open(check, "w", encoding="utf-8") as c:
            json.dump(checker_data, c, indent="\t")

        # metrics
        metric_data = {
            "error_count": int,
            "main": {}
        }
        ctl = gram_out_json.get_cleaned_token_list()
        for og_sent, inner_dict in checker_data.items():
            if inner_dict["edited"] == True:
                inner_data = gram_out_json.get_scrs_tok(inner_dict, ctl)
                metric_data["main"][og_sent] = inner_data
            else:
                metric_data["main"][og_sent] = {"edited": False, "corrected_sentence": inner_dict["fin_sentence"]}

        error_count = 0
        for og in metric_data["main"]:
            v = metric_data["main"][og]
            if v["edited"] == True:
                error_count += len(v["action_tag"])
        metric_data["error_count"] = error_count

        # Run this part if you want the metric json file
        # metric = os.path.join(gector_path, "metric", "metric.json")
        # with open(metric, "w", encoding="utf-8") as r:
        #     json.dump(metric_data, r, indent="\t")

        # Final output
        phase = "phase_2"
        out_path = os.path.join(gector_path, "real", f"grammar_{phase}.json")
        return gram_out_json.create_json(phase=phase, out_path=out_path, error_count=error_count, check_data=checker_data)
    except Exception as e:
        return {"text": None, "status": f"Error: {str(e)}"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8888)
