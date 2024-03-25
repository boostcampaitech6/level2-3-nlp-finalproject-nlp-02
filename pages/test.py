import streamlit as st
from streamlit_mic_recorder import mic_recorder
import base64
import requests

#remove navigation bar
st.markdown("""
    <style>
        section[data-testid="stSidebar"][aria-expanded="true"]{
            display: none; 
        }
    </style>
    """, unsafe_allow_html=True)


test = "http://mopic.test/api/test"


st.title("Daily Test")
st.image("AVA.png", caption="문제를 두 번 들려드린 후 바로 녹음을 시작해주세요.", width=300)


#remove image expansion
st.markdown("""
    <style>
        [data-testid="StyledFullScreenButton"]{
            visibility: hidden;
        }
    </style>
    """, unsafe_allow_html=True)


# When "listen" button is pressed, Convert .wav->html tag to autoplay
def autoplay_audio(file_path: str):
    with open(file_path, "rb") as audio_file:
        audio_bytes = audio_file.read()
        audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")
        audio_html = f'<audio autoplay><source src="data:audio/wav;base64,{audio_base64}" type="audio/wav"></audio>'
        st.markdown(audio_html, unsafe_allow_html=True)


def save_recording(audio_data):
    files = {"file": ("recording4.wav", audio_data, "audio/wav")}
    response = requests.post(test, files=files)


def callback():
    # Check 'my_recorder_output' in st.session_state
    if "my_recorder_output" in st.session_state:
        audio_data = st.session_state.my_recorder_output["bytes"]
        if audio_data is not None:
            save_recording(audio_data)
            st.audio(audio_data, format="audio/wav")
        else:
            st.error("오디오 데이터를 찾을 수 없습니다.")


def save_recording_locally(audio_data):
    # Convert the audio data to a downloadable file
    audio_file = base64.b64encode(audio_data).decode()
    href = f'<a href="data:file/wav;base64,{audio_file}" download="recording.wav">Download recording</a>'
    st.markdown(href, unsafe_allow_html=True)


# question file path
q_audio_path_1 = "q_1.wav"
q_audio_path_2 = "q_2.wav"
q_audio_path_3 = "q_3.wav"

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
st.markdown(button_style, unsafe_allow_html=True)

cols = st.columns([1, 1, 1, 11])
recorder_holder = st.empty()  # Fix the position of the "Start recording" button


def main() -> None:
    # each question button
    with cols[0]:
        if st.button("1"):
            autoplay_audio(q_audio_path_1)

    with cols[1]:
        if st.button("2"):
            autoplay_audio(q_audio_path_2)

    with cols[2]:
        if st.button("3"):
            autoplay_audio(q_audio_path_3)

    # Start & stop recording buttons
    with recorder_holder.container():
        mic_recorder(
            start_prompt="녹음 시작",
            stop_prompt="다음",
            just_once=True,
            key="my_recorder",
            use_container_width=True,
            format="wav",
            callback=callback,
        )


if __name__ == "__main__":
    main()



