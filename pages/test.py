import streamlit as st
from streamlit_mic_recorder import mic_recorder
import base64
import requests
import io

# Define the endpoint URL of the server where you want to save the recording
test = "http://000.000.000.000:0000/test"

st.title("Daily Test")
st.image("AVA.png", caption="문제를 두 번 들려드린 후 바로 녹음을 시작해주세요.", width=300)


# 1. "듣기" 버튼 눌렀을 때 문제 자동재생 되도록 .wav->html 태그로 변환
def autoplay_audio(file_path: str):
    with open(file_path, "rb") as audio_file:
        audio_bytes = audio_file.read()
        audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
        audio_html = f'<audio autoplay><source src="data:audio/wav;base64,{audio_base64}" type="audio/wav"></audio>'
        st.markdown(audio_html, unsafe_allow_html=True)


def save_recording(audio_data):
    files = {'audio': ('recording.wav', audio_data, 'audio/wav')}
    response = requests.post(test, files=files)
    if response.ok:
        st.success("The recording was successfully saved.")
    else:
        st.error("Failed to save the recording.")


def callback():
    # st.session_state에서 'my_recorder_output'을 확인합니다.
    if 'my_recorder_output' in st.session_state:
        audio_data = st.session_state.my_recorder_output['bytes']
        if audio_data is not None:
            save_recording(audio_data)
            st.audio(audio_data, format='audio/wav')
        else:
            st.error("오디오 데이터를 찾을 수 없습니다.")

def save_recording_locally(audio_data):
    # Convert the audio data to a downloadable file
    audio_file = base64.b64encode(audio_data).decode()
    href = f'<a href="data:file/wav;base64,{audio_file}" download="recording.wav">Download recording</a>'
    st.markdown(href, unsafe_allow_html=True)


q_audio_path_1 = 'q_1.wav'  # question file path
q_audio_path_2 = 'q_2.wav'  # question file path
q_audio_path_3 = 'q_3.wav'  # question file path

# 버튼모양
button_style = """
<style>
div.stButton > button:first-child {
    margin: 0px 5px;
    width: 100%;
}
</style>
"""
st.markdown(button_style, unsafe_allow_html=True)

# 녹음 시작 버튼을 위한 홀더 생성
recorder_holder = st.empty()

# 버튼 스타일 적용
button_style = """
<style>
div.stButton > button {
    display: block;
    margin: 0px 5px ;
    width: 50%;
}
</style>
"""
st.markdown(button_style, unsafe_allow_html=True)

cols = st.columns([1, 1, 1, 11])
recorder_holder = st.empty()  # "녹음 시작" 버튼을 위한 홀더


def main() -> None:
    # 1. "듣기" 누르면 문제 자동재생
    with cols[0]:
        if st.button("1"):
            autoplay_audio(q_audio_path_1)
            # recorder_holder.empty()
            # with recorder_holder.container():
            #     mic_recorder(start_prompt="녹음 시작", stop_prompt="녹음 중지", key='my_recorder', callback=callback)

    with cols[1]:
        if st.button("2"):
            autoplay_audio(q_audio_path_2)
            # recorder_holder.empty()
            # with recorder_holder.container():
            #     mic_recorder(start_prompt="녹음 시작", stop_prompt="녹음 중지", key='my_recorder', callback=callback)
    with cols[2]:
        if st.button("3"):
            autoplay_audio(q_audio_path_3)
            # recorder_holder.empty()
            # with recorder_holder.container():
            #     mic_recorder(start_prompt="녹음 시작", stop_prompt="녹음 중지", key='my_recorder', callback=callback)

    # 2. 녹음 시작 버튼
    recorder_holder = st.empty()
    recorder_holder.empty()
    with recorder_holder.container():
        mic_recorder(start_prompt="녹음 시작", stop_prompt="녹음 중지", key='my_recorder', callback=callback)


if __name__ == "__main__":
    main()