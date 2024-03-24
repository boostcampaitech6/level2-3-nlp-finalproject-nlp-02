import requests
import streamlit as st

st.markdown("""
    <style>
        section[data-testid="stSidebar"][aria-expanded="true"]{
            display: none;
        }
    </style>
    """, unsafe_allow_html=True)


response = requests.get(
    url=f"https://mopic.today/api/me/result/{st.session_state['date']}",
    headers={"access_token": st.session_state["token"]["access_token"]},
)
if response.status_code == 200:
    data = response.json()

st.title(f"{data['createdDate']} 시험 결과")

st.markdown(
    """
<style>
.score {
    font-size:30px !important;
}
</style>
""",
    unsafe_allow_html=True,
)

st.markdown(
    f"당신의 예상 등급은 <span class='score'>{data['finalscore']}</span> 입니다.",
    unsafe_allow_html=True,
)

tab1, tab2, tab3 = st.tabs(["1번", "2번", "3번"])
# TODO: 해당 시험의 날짜를 받아오도록 함수 변경

with tab1:
    question_response = requests.get(
        url=f"https://mopic.today/api/me/result/{st.session_stae['date']/1}",
        headers={"access_token": st.session_state["token"]["access_token"]},
    )
    
    if question_response.status_code == 200:
        question_data = question_response.json()

        st.header(f"{question_data['q_num']}")
        st.write(question_data)


with tab2:
    question_response = requests.get(
        url=f"https://mopic.today/api/me/result/{st.session_stae['date']/2}",
        headers={"access_token": st.session_state["token"]["access_token"]},
    )
    
    if question_response.status_code == 200:
        question_data = question_response.json()

        st.header(f"{question_data['q_num']}")
        st.write(question_data)

with tab3:
    question_response = requests.get(
        url=f"https://mopic.today/api/me/result/{st.session_stae['date']/3}",
        headers={"access_token": st.session_state["token"]["access_token"]},
    )
    
    if question_response.status_code == 200:
        question_data = question_response.json()

        st.header(f"{question_data['q_num']}")
        st.write(question_data)
