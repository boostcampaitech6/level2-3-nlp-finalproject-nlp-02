import json
import shutil
from pprint import pprint
from typing import List

import uvicorn
from fastapi import Body, FastAPI, File, Form, HTTPException, UploadFile
from pydub import AudioSegment
from typing_extensions import Annotated

app = FastAPI()


def get_WPM(wav_file, text):
    audio = AudioSegment.from_wav(wav_file.filename)
    timestamp = text
    # 오디오 길이 (밀리초 단위)
    audio_length_ms = len(audio)
    # 초 단위로 변환
    audio_length_sec = audio_length_ms / 1000
    # 분 단위로 변환
    audio_length_min = audio_length_sec / 60

    WPM = round((len(timestamp) / audio_length_min), 2)
    return WPM, audio_length_sec


def get_pause_list(text):
    # with open(text, 'r') as f:
    #     data = json.load(f)
    # timestamp = data['word_timestamp']
    timestamp = text
    # print(timestamp)
    pause = 0
    pause_list = [item for item in timestamp if "start" in item and "end" in item]
    # print(pause_list)
    for i in range(len(pause_list) - 1):
        if len(pause_list[i]) != 4 or len(pause_list[i + 1]) != 4:
            pause = pause
        else:
            pause += pause_list[i + 1]["start"] - pause_list[i]["end"]
    return pause


def slice_btw(text):
    data = []
    for i in range(len(text) - 1):
        if len(text[i]) != 4 or len(text[i + 1]) != 4:
            pass
        else:
            data.append(text[i + 1]["start"] - text[i]["end"])
    return data


# 연속된 0.25 이하의 값을 갖는 요소들의 길이를 저장할 리스트


# 연속된 0.25 이하의 값을 갖는 요소들의 길이를 계산하여 리스트에 추가하는 함수
def count_consecutive_low_values(data):
    consecutive_lengths = []
    consecutive_count = 0

    for value in data:
        if value <= 0.25:
            consecutive_count += 1
        else:
            if consecutive_count > 0:
                consecutive_lengths.append(consecutive_count)
            consecutive_count = 0

    if consecutive_count > 0:
        consecutive_lengths.append(consecutive_count)
    return consecutive_lengths


@app.post("/upload/")
async def get_fluency(
    wav_file: Annotated[UploadFile, File()],
    # text: List[str],
    text: Annotated[str, Form()],
):
    # WAV 파일 로드
    # WAV 파일 저장
    with open(wav_file.filename, "wb") as buffer:
        shutil.copyfileobj(wav_file.file, buffer)

    ls = json.loads(text)

    # get word per min
    WPM, audio_length = get_WPM(wav_file, ls)

    # get pause rate
    n_pause = get_pause_list(ls)
    paused_rate = (n_pause / audio_length) * 100
    pause_rate = round(paused_rate, 2)

    # get mean length of run
    data = slice_btw(ls)
    mlr_counts = count_consecutive_low_values(data)
    if len(mlr_counts) == 0:
        average_mlr = 0
    else:
        average_mlr = round(sum(mlr_counts) / len(mlr_counts), 2)

    return {"WPM": WPM, "Pause_rate": pause_rate, "mlr_count": average_mlr}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8888)


# 연속된 0.25 이하의 값을 갖는 요소들의 길이 계산

# 연속된 부분 리스트들의 길이 출력
# print("연속된 부분 리스트들의 길이:", mlr_counts)
# 총 개수의 평균 계산
# average_mlr = sum(mlr_counts) / len(mlr_counts)
# print("총 개수의 평균:", average_mlr)
# json_object = {
#     "average_mlr":average_mlr
#     }
# with open('output.json', 'w') as f:
#     json.dump(json_object, f, indent=2)
