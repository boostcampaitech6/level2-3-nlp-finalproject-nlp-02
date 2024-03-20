import base64
import os
import threading
import wave

import pyaudio
import requests
import streamlit as st

# 전역 변수 설정
is_recording = False
frames = []


test = "http://mopic.test/api/test"

st.title("Daily Test")
st.image("AVA.png", caption="문제를 두 번 들려드린 후 바로 녹음을 시작해주세요.", width=300)

# 1. "듣기" 버튼 눌렀을 때 문제 자동재생 되도록 .wav->html 태그로 변환
def autoplay_audio(file_path: str):
    with open(file_path, "rb") as audio_file:
        audio_bytes = audio_file.read()
        audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")
        audio_html = f'<audio autoplay><source src="data:audio/wav;base64,{audio_base64}" type="audio/wav"></audio>'
        st.markdown(audio_html, unsafe_allow_html=True)


# 2. 녹음
def recording():
    global is_recording, frames
    is_recording = True
    frames = []

    # 오디오 설정
    chunk = 1024
    format = pyaudio.paInt16
    channels = 1
    rate = 16000

    p = pyaudio.PyAudio()

    stream = p.open(
        format=format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk
    )

    # 녹음 중 데이터를 frames array에 저장하기
    while is_recording:
        data = stream.read(chunk)
        frames.append(data)

    # stream 정지 & 종료
    stream.stop_stream()
    stream.close()
    p.terminate()


# 3. 정지&저장
def stop_and_save_recording(filename):
    global is_recording
    is_recording = False
    if frames:
        wf = wave.open(filename, "wb")
        wf.setnchannels(2)
        wf.setsampwidth(pyaudio.PyAudio().get_sample_size(pyaudio.paInt16))
        wf.setframerate(16000)
        wf.writeframes(b"".join(frames))
        wf.close()
        st.success(f"Recording saved as {filename}")
    else:
        st.error("No recording to save.")


# TODO: 옆의 이미지 확장 버튼 숨기기

# TODO: 이하의 로직이 3번 반복되도록 작성
# qlist = requests.get(url=test)

# if st.button("재생"):
#     # TTS 로 문제 읽기
#     pass
#
#     audio = audiorecorder("Start Record", "Next")
#     # TODO: 자동으로 녹음 시작되면 좋음.
#
#     if len(audio) > 0:
#         # 저장
#         wav = audio.export("test.wav", format="wav")
#         files = {"file": (wav.name, wav, "multipart/form-data")}
#         response = requests.post(url=test, files=files)
#
#         if response.status_code == 200:
#
#             data = response.json()
#             st.write(data)


def main() -> None:
    q_audio_path = "test_q.wav"  # question file path

    # 1. "듣기" 누르면 문제 자동재생
    if st.button("듣기"):
        autoplay_audio(q_audio_path)

    # 2. "녹음 시작" 누르면 녹음 시작
    if st.button("녹음 시작"):
        threading.Thread(target=recording).start()
        st.write("Recording...")

    # 3. "다음" 누르면 녹음 정지 및 저장
    if st.button("다음"):
        stop_and_save_recording("output.wav")


if __name__ == "__main__":
    main()
