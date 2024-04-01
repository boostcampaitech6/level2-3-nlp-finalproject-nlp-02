import shutil
from typing import List

import torch
import uvicorn
import whisperx
from fastapi import Body, FastAPI, File, HTTPException, UploadFile
from PIL import Image
from torchvision import transforms

app = FastAPI()

model = whisperx.load_model(
    "large-v3",
    "cuda",
    language="en",
    compute_type="float16",
    download_root="/dev/shm/whisperx",
)
model_a, metadata = whisperx.load_align_model(language_code="en", device="cuda")


# 라우터 정의
@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    try:
        with open(file.filename, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        wav_path = file.filename
        output_path = wav_path[:-4]
        audio_file = wav_path
        batch_size = 16  # reduce if low on GPU mem

        # 1. call first model
        audio = whisperx.load_audio(audio_file)
        result = model.transcribe(audio, batch_size=batch_size)
        text = ""
        for i in range(len(result["segments"])):
            text = "".join([text, result["segments"][i]["text"]])
        # print(text) # before alignment

        # 2. Align whisper output
        result1 = whisperx.align(
            result["segments"],
            model_a,
            metadata,
            audio,
            device="cuda",
            return_char_alignments=False,
        )
        ls = []
        for i in range(len(result1["segments"])):
            for j in range(len(result1["segments"][i]["words"])):
                ls.append(result1["segments"][i]["words"][j])
        json_object = {"transcription": text, "word_timestamp": ls}
        # print(json_object) # after alignment

        return json_object
    except Exception as e:
        return {"filename": None, "status": f"Error: {str(e)}"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8888)
