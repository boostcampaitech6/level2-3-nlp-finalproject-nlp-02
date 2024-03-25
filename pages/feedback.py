import requests
import streamlit as st

def fix_sentence(tagged_list):
    if tagged_list:
        for tagged in tagged_list:
            with st.expander(tagged["sentence"]):
                for i in range(len(tagged["tag"])):
                    st.write(tagged["ref_word"][i], tagged["tag"][i], tagged["category"][i], tagged["grammar_description"][i])
    else:
        return st.write("틀린 문장이 없네요! 아주 잘 하셨어요.")

def make_layout(question_data):
    by_text, by_speaking = st.tabs(["텍스트", "말하기"])

    with by_text:
        grammar = question_data["grammar"]["phase_2"]
        st.subheader("grammar")
        st.markdown(f"전체 발화 문장 중 올바른 문법 사용 비율은 **{grammar["score"]}%** 입니다.")

        with st.container(height=300):
            st.markdown(grammar["original_passage"])

        fix_sentence(grammar["tag_grammar_info"])

        st.subheader("coherence")
        st.markdown(f"- 고객님의 질문에 대한 답변의 주제 적합성은 **{question_data["coherence"]}**입니다")
        st.subheader("complexity")
        st.markdown(f"{question_data["complexity"]}")

    with by_speaking:
        st.markdown(f"전체 발화 중 잘못된 발음 없이 명확하게 발음한 비율은 **{question_data["mpr"]}%** 입니다.")
        st.markdown(f"연속으로 발화한 평균 단어 수는 **{question_data["mlr"]}개** 입니다.")
        st.markdown(f"전체 발화 중 pause 비율은 **{question_data["pause"]}%** 입니다.")


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
questions = requests.get(url="http://mopic.today/api/test").json()

with tab1:
    question_response_1 = requests.get(
        url=f"http://mopic.today/api/me/result/{st.session_state['date']}/1",
        headers={"access_token": st.session_state["token"]["access_token"]},
    )

    if question_response_1.status_code == 200:
        question_data_1 = question_response_1.json()

        st.write(f"{question_data_1['q_num']}. {questions['q1']}")
    
        make_layout(question_data_1)

with tab2:
    question_response_2 = requests.get(
        url=f"http://mopic.today/api/me/result/{st.session_state['date']}/2",
        headers={"access_token": st.session_state["token"]["access_token"]},
    )
    
    if question_response_2.status_code == 200:
        question_data_2 = question_response_2.json()

        st.write(f"{question_data_2['q_num']}. {questions['q2']}")
        make_layout(question_data_2)

with tab3:
    question_response_3 = requests.get(
        url=f"http://mopic.today/api/me/result/{st.session_state['date']}/3",
        headers={"access_token": st.session_state["token"]["access_token"]},
    )
    
    if question_response_3.status_code == 200:
        question_data_3 = question_response_3.json()

        st.write(f"{question_data_3['q_num']}. {questions['q3']}")
        make_layout(question_data_3)