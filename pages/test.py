import base64

import requests
import streamlit as st
from streamlit_mic_recorder import mic_recorder

# remove navigation bar
st.markdown(
    """
    <style>
        section[data-testid="stSidebar"][aria-expanded="true"]{
            display: none; 
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# Define the endpoint URL of the server where you want to save the recording
test = "https://mopic.today/api/test"


st.title("Daily Test")
st.image("AVA.png", caption="문제를 두 번 들려드린 후 바로 녹음을 시작해주세요.", width=300)


# remove image expansion
st.markdown(
    """
    <style>
        [data-testid="StyledFullScreenButton"]{
            visibility: hidden;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# When "listen" button is pressed, Convert .wav->html tag to autoplay
def autoplay_audio(file_path: str):
    with open(file_path, "rb") as audio_file:
        audio_bytes = audio_file.read()
        audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")
        audio_html = f'<audio autoplay><source src="data:audio/wav;base64,{audio_base64}" type="audio/wav"></audio>'
        st.markdown(audio_html, unsafe_allow_html=True)


# question_num : 사용자 음성파일 이름변경을 위한 변수
def save_recording(audio_data, question_num):
    files = {"file": (f"test{question_num}.wav", audio_data, "audio/wav")}
    response = requests.post(
        url=test,
        files=files,
        headers={"Access-Token": st.session_state["token"]["access_token"]},
    )
    # print(response.text)
    if response.status_code == 200:
        st.success("The recording was successfully saved.")
    else:
        st.error("Failed to save the recording.")


def callback():
    question_num = st.session_state.question_num
    # Check 'my_recorder_output' in st.session_state
    if "my_recorder_output" in st.session_state:
        audio_data = st.session_state.my_recorder_output["bytes"]
        if audio_data is not None:
            save_recording(audio_data, question_num)
            st.audio(audio_data, format="audio/wav")
        else:
            st.error("오디오 데이터를 찾을 수 없습니다.")


# button shape
button_style = """
<style>
div.stButton > button:first-child {
    margin: 0px 5px;
    width: 100%;
}
</style>
"""

st.markdown(button_style, unsafe_allow_html=True)

# Apply a button styles
button_style = """
<style>
div.stButton > button {
    display: block;
    margin: 0px 5px ;
    width: 50%;
}
</style>
"""

cols = st.columns([1, 1, 1, 11])
recorder_holder = st.empty()  # "녹음 시작" 버튼 위치 고정


# 질문 오디오 파일 경로
q_audio_paths = {
    "1": "/home/beom/mopic/tts_data/2024-03-26_q1.wav",
    "2": "/home/beom/mopic/tts_data/2024-03-26_q2.wav",
    "3": "/home/beom/mopic/tts_data/2024-03-26_q3.wav",
}

if "question_clicked" not in st.session_state:
    st.session_state.question_clicked = None


# replay_count를 세션 상태로 초기화
if "replay_count" not in st.session_state:
    st.session_state.replay_count = 0

# 오디오가 이미 재생되었는지 여부를 확인하기 위한 상태 초기화
if "played_1" not in st.session_state:
    st.session_state["played_1"] = False
if "played_2" not in st.session_state:
    st.session_state["played_2"] = False
if "played_3" not in st.session_state:
    st.session_state["played_3"] = False

replay_limit = 1  # 재생 제한 횟수

with cols[0]:
    if st.button("1") and not st.session_state["played_1"]:
        st.session_state.question_num = 1
        st.session_state.question_clicked = str("1")
        autoplay_audio(q_audio_paths["1"])
        st.session_state["played_1"] = True
        st.session_state.replay_count = 0

with cols[1]:
    if st.button("2") and not st.session_state["played_2"]:
        st.session_state.question_num = 2
        st.session_state.question_clicked = str("2")
        autoplay_audio(q_audio_paths["2"])
        st.session_state["played_2"] = True
        st.session_state.replay_count = 0

with cols[2]:
    if st.button("3") and not st.session_state["played_3"]:
        st.session_state.question_num = 3
        st.session_state.question_clicked = str("3")
        autoplay_audio(q_audio_paths["3"])
        st.session_state["played_3"] = True
        st.session_state.replay_count = 0

if st.session_state.question_clicked:
    # 'Replay' 버튼 추가
    if st.button("Replay", help="문제를 다시 듣고 싶다면 클릭해주세요."):
        if st.session_state.replay_count < replay_limit:
            autoplay_audio(q_audio_paths[st.session_state.question_clicked])
            st.session_state.replay_count += 1
        else:
            st.warning("재생 횟수를 초과하였습니다.", icon="⚠️")

    # 녹음 버튼 추가
    mic_recorder(
        start_prompt="녹음 시작",
        stop_prompt="다음",
        just_once=True,
        key="my_recorder",
        use_container_width=True,
        format="wav",
        callback=callback,
    )
