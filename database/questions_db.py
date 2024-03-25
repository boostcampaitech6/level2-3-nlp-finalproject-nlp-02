import os
import json
from datetime import datetime, timedelta

import psycopg2
import yaml

from transformers import SpeechT5Processor, SpeechT5ForTextToSpeech, SpeechT5HifiGan
from datasets import load_dataset
import torch
import soundfile as sf


def load_config(filename):
    with open(filename, "r") as config_file:
        config = yaml.safe_load(config_file)
    return config


def create_date(data):
    pattern = "%Y-%m-%d"
    start_date = datetime(2024, 3, 21).date()
    num_values = len(data)
    interval = timedelta(days=1)
    date_series = [start_date + i * interval for i in range(num_values)]

    return date_series


def run_tts(input_text, save_path):
    # 모델 경로 지정
    model_save_path = "microsoft/speecht5_tts"
    vocoder_save_path = "microsoft/speecht5_hifigan"
    processor_save_path = "microsoft/speecht5_tts"

    # 모델 불러오기
    processor = SpeechT5Processor.from_pretrained(
        processor_save_path, cache_dir="/dev/shm"
    )
    vocoder = SpeechT5HifiGan.from_pretrained(vocoder_save_path, cache_dir="/dev/shm")
    model = SpeechT5ForTextToSpeech.from_pretrained(
        model_save_path, cache_dir="/dev/shm"
    )

    inputs = processor(text=input_text, return_tensors="pt")

    # load xvector containing speaker's voice characteristics from a dataset
    embeddings_dataset = load_dataset(
        "Matthijs/cmu-arctic-xvectors", split="validation"
    )
    speaker_embeddings = torch.tensor(embeddings_dataset[7306]["xvector"]).unsqueeze(0)

    speech = model.generate_speech(
        inputs["input_ids"], speaker_embeddings, vocoder=vocoder
    )

    sf.write(save_path, speech.numpy(), samplerate=16000)


config = load_config("../config.yaml")
db_config = config.get("database")

host_ip = db_config["dbname"][32:47]
db = db_config["dbname"][48:55]
user = db_config["username"]
password = db_config["password"]

conn = psycopg2.connect(host=host_ip, database=db, user=user, password=password)

cur = conn.cursor()

qdata_path = "../data/generated_question.json"
tts_save_path = "../tts_data"
tts_db_path = "level2-3-nlp-finalproject-nlp-02/tts_data"
with open(qdata_path, "r") as f:
    data = json.load(f)
    date = create_date(data)
    for idx, line in enumerate(data):
        today = date[idx]
        q1 = line["Q1"]
        q2 = line["Q2"]
        q3 = line["Q3"]

        # 경로에 wav파일이 존재하면
        if os.path.exists(os.path.join(tts_save_path, f"{today}_q1.wav")):
            run_tts(q1, os.path.join(tts_save_path, f"{today}_q1.wav"))
        if os.path.exists(os.path.join(tts_save_path, f"{today}_q2.wav")):
            run_tts(q2, os.path.join(tts_save_path, f"{today}_q2.wav"))
        if os.path.exists(os.path.join(tts_save_path, f"{today}_q3.wav")):
            run_tts(q3, os.path.join(tts_save_path, f"{today}_q3.wav"))

        q1_wav_db_path = os.path.join(tts_db_path, f"{today}_q1.wav")
        q2_wav_db_path = os.path.join(tts_db_path, f"{today}_q2.wav")
        q3_wav_db_path = os.path.join(tts_db_path, f"{today}_q3.wav")

        # row가 이미 존재하는지 확인
        cur.execute("SELECT EXISTS(SELECT 1 FROM questions WHERE date=%s)", (today,))
        if cur.fetchone()[0]:
            print(f"Question with data {today} already exists in the database.")
            continue

        query = "INSERT INTO questions (date, q1, q2, q3, q1_wav, q2_wav, q3_wav) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        data = (today, q1, q2, q3, q1_wav_db_path, q2_wav_db_path, q3_wav_db_path)
        cur.execute(query, data)
        conn.commit()

cur.close()
conn.close()
