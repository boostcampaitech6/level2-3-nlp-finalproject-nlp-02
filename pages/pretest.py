import streamlit as st
from audiorecorder import audiorecorder

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


st.write("시험은 하루에 한 번만 볼 수 있습니다. 중도 이탈 시 데이터는 저장되지 않습니다.")
st.write("문제 음성은 총 두 번 들려드립니다.")
st.write("조용한 환경에서 응시해주세요. 보다 정확한 결과가 나옵니다.")
st.write("마이크를 허용해주시고, 아래 버튼으로 녹음하여 녹음이 제대로 되는지 확인하세요.")

voicecheck = audiorecorder("check your voice")
st.session_state.my_recorder_output = None
st.session_state.question_num = None


if len(voicecheck) > 0:
    # To play audio in frontend:
    st.audio(voicecheck.export().read())

    if st.button("응시"):
        st.switch_page(page="./pages/test.py")
