import asyncio
import concurrent.futures
import json
import re
import os
from typing import Annotated

import requests
import uvicorn
import yaml
from fastapi import FastAPI, File, Form, UploadFile
from openai import OpenAI

app = FastAPI()


def load_config(filename):
    with open(filename, "r") as config_file:
        config = yaml.safe_load(config_file)
    return config


config = load_config("config.yaml")
model_config = config.get("models")
server_config = config.get("servers")
# 0.chatgpt 프롬프팅 구간
api_key = model_config.get("gpt_api_key")
client_1 = OpenAI(api_key=api_key)
client_1.fine_tuning.jobs.retrieve(model_config.get("gpt_model_ft1"))
client_2 = OpenAI(api_key=api_key)
client_2.fine_tuning.jobs.retrieve(model_config.get("gpt_model_ft2"))

# 1.send_wav_to_STT
async def whisperx(file_path, server_url):
    print("Run whisperx")
    with open(file_path, "rb") as file:
        files = {"file": file}
        response = requests.post(server_url, files=files)
    print("Done whisperx")
    return response.json()  # 반환된 텍스트 출력


# 2.wav_json_to_PR
def phoneme_detection(file_path, json_data, server_url):
    print("Run phoneme_detection")
    with open(file_path, "rb") as wav_file:
        files = {"wav_file": wav_file}
        data = {"text": json_data["transcription"]}
        response = requests.post(server_url, files=files, data=data)
    assert response.status_code == 200, response.text
    print("Done phoneme_detection")
    return response.json()


# 3.get_pause,
def get_pause(file_path, json_data, server_url):
    print("Run get_pause")
    with open(file_path, "rb") as wav_file:
        files = {"wav_file": wav_file}
        data = {"text": json.dumps(json_data["word_timestamp"])}
        # data = {"text": json_data['transcription']}
        response = requests.post(server_url, files=files, data=data)
    assert response.status_code == 200, response.text
    print("Done get_pause")
    return response.json()


def check_grammar(json_data, server_url):
    print("Run check_grammar")
    data = {"text": json_data["transcription"]}
    response = requests.post(server_url, data=data)
    assert response.status_code == 200, response.text
    print("Done check_grammar")
    return response.json()


# 4.GPT Json transcript coherence 생성
def check_coherence(json_data, question):
    print("Run check_coherence")
    answer = "{" + json_data["transcription"] + "}"
    # question = 추후 예정
    question = question
    content = ", ".join([question, answer])
    # print(content)
    response = client_1.chat.completions.create(
        model="ft:gpt-3.5-turbo-0125:personal::8yvBw03H",
        messages=[
            {"role": "system", "content": "질문에 대한 대답 스크립트가 입력되었을 때 문맥이 적합한지 평가"},
            {"role": "assistant", "content": "{높음, 중간, 낮음} 중 하나로 평가"},
            # {"role": "user", "content": "{How has your interest in plays changed over the last few years? What kind of play did you like in the past? What about now?}, {Okay, Lets talk about My taste in concerts... Actually, I have seen a lot of concerts. Right. Nowadays, I love k-pop concerts such as BTS concerts, Aespa concerts, Blackpink concerts, and whatever. K-pop concerts are a trend these days. And there are a lot of k-pop concerts in Korea. Those concerts are so fun and spectacular. But in the past, Um... yeah, I liked piano concerts. Because the first concert I have seen in my life is called Classic. That concert was a piano concert. It was so impressive and touched me. But I like k-pop concerts now. You know, it makes me feel like Im a k-pop star. What about you?}" }
            {"role": "user", "content": content},
        ],
    )
    res_json = json.loads(response.json())
    print("Done check_coherence")
    return res_json["choices"][0]["message"]["content"]


# 5.GPT JSON transccript complexity 생성
def check_complexity(json_data):
    print("Run check_complexity")
    answer = json_data["transcription"]
    response = client_2.chat.completions.create(
        model = "gpt-4-turbo-preview",
        messages=[
                {"role": "system", "content": "Count the Compound Sentence, Complex Sentence, and Simple Sentence, Incomplete Sentence in the input script, and give simple feedback in korean on the composition according to the sentence ratio"},
                {"role": "assistant", "content": "- Compound sentence: 1개 \n - Complexity sentence: 3개 \n - Simple Sentence: 4개 \n\n - Not a sentence: 0개 \n\n Feedback: \"전체적인 구성은 좋지만 Compound 문장을 더 만들어볼까요?\""},
                {"role": "user", "content": answer},
        ],
    )
    res_json = json.loads(response.json())
    output = res_json["choices"][0]["message"]["content"]
    # print(output)

    output  = re.findall(r'(?<=: ).*$', output)
    print("Done check_complexity")
    return output


@app.post("/run_inference/")
# 비동기 병렬처리
async def process_responses(
    # file: UploadFile = File(...)
    data: dict
):

    # 이후에 유저 인풋 wav_binary로 교체
    file_path_1 = data.get("data")
    question = data.get("question")
    server_url_1 = server_config.get("server_url_1")
    server_url_2 = server_config.get("server_url_2")
    server_url_3 = server_config.get("server_url_3")
    server_url_4 = server_config.get("server_url_4")

    response_1 = await whisperx(file_path_1, server_url_1)

    loop = asyncio.get_event_loop()
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        tasks = [
            loop.run_in_executor(
                executor, phoneme_detection, file_path_1, response_1, server_url_2
            ),
            loop.run_in_executor(executor, check_grammar, response_1, server_url_3),
            loop.run_in_executor(executor, check_coherence, response_1, question),
            loop.run_in_executor(executor, check_complexity, response_1),
            loop.run_in_executor(
                executor, get_pause, file_path_1, response_1, server_url_4
            ),
        ]
        responses = {}
        task_names = ["mpr", "grammar", "coherence", "complexity", "get_fluency"]

        for name, task in zip(task_names, tasks):
            result = await task
            if name == "get_fluency":
                # return {"WPM":WPM, "Pause_rate":pause_rate, "mlr_count": average_mlr}
                responses["wpm"] = result["WPM"]
                responses["pause"] = result["Pause_rate"]
                responses["mlr"] = result["mlr_count"]
            else:
                responses[f"{name}"] = result
        return responses


#
if __name__ == "__main__":
    # loop = asyncio.get_event_loop()
    # responses = loop.run_until_complete(process_responses())
    # print(responses)
    uvicorn.run(app, host="localhost", port=8001)
