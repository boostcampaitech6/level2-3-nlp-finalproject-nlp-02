import streamlit as st
import requests
from audiorecorder import audiorecorder

test = "http://000.000.000.000:0000/test"

st.title("Daily Test")
st.image("AVA.png", caption="문제를 두 번 들려드린 후 바로 녹음을 시작해주세요.", width=300)
# TODO: 옆의 이미지 확장 버튼 숨기기

# TODO: 이하의 로직이 3번 반복되도록 작성
# qlist = requests.get(url=test)

if st.button("재생"):
    # TTS 로 문제 읽기
    pass

    audio = audiorecorder("Start Record", "Next")
    # TODO: 자동으로 녹음 시작되면 좋음.

    if len(audio) > 0:
        # 저장
        wav = audio.export("test.wav", format="wav")
        files = {"file": (wav.name, wav, "multipart/form-data")}
        response = requests.post(url=test, files=files)

        if response.status_code == 200:

            data = response.json()
            st.write(data)
