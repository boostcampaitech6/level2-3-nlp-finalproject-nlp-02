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
    url=f"http://mopic.today/api/me/result/{st.session_state['date']}",
    headers={"access_token": st.session_state["token"]["access_token"]},
)
if response.status_code == 200:
    data = response.json()

st.title(f"{data['date']} 시험 결과")

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
    f"당신의 예상 등급은 <span class='score'>{data['score']}</span> 입니다.",
    unsafe_allow_html=True,
)

tab1, tab2, tab3 = st.tabs(["1번", "2번", "3번"])


with tab1:
    question_response_1 = requests.get(
        url=f"https://mopic.today/api/me/result/{st.session_state['date']}/1",
        headers={"access_token": st.session_state["token"]["access_token"]},
    )
    
    if question_response_1.status_code == 200:
        question_data_1 = question_response_1.json()

        st.header(f"{question_data_1['q_num']}")
        st.write(question_data_1)


with tab2:
    question_response_2 = requests.get(
        url=f"http://mopic.today/api/me/result/{st.session_state['date']}/2",
        headers={"access_token": st.session_state["token"]["access_token"]},
    )
    
    if question_response_2.status_code == 200:
        question_data_2 = question_response_2.json()

        st.header(f"{question_data_2['q_num']}")
        st.write(question_data_2)

with tab3:
    question_response_3 = requests.get(
        url=f"http://mopic.today/api/me/result/{st.session_state['date']}/3",
        headers={"access_token": st.session_state["token"]["access_token"]},
    )
    
    if question_response_3.status_code == 200:
        question_data_3 = question_response_3.json()

        st.header(f"{question_data_3['q_num']}")
        st.write(question_data_3)
