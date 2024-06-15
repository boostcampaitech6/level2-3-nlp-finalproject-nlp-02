import requests
import streamlit as st


def fix_sentence(tagged_list):
    if tagged_list:
        for tagged in tagged_list:
            with st.expander(tagged["sentence"]):
                for i in range(len(tagged["grammar_description"])):
                    if tagged["grammar_description"][i] == "PLURAL TO SINGULAR VERB":
                        st.write(f"복수형 동사를 단수형으로 바꿔주세요.")
                    elif (
                        tagged["grammar_description"][i] == "PRESENT TO PAST PARTICIPLE"
                    ):
                        st.write(f"시제를 현재에서 과거분사로 바꿔주세요.")
                    elif tagged["grammar_description"][i] == "PRESENT TO PAST TENSE":
                        st.write(f"시제를 현재에서 과거로 바꿔주세요.")
                    elif (
                        tagged["grammar_description"][i]
                        == "PRESENT TO PRESENT PARTICIPLE"
                    ):
                        st.write(f"시제를 현재에서 현재 진행형으로 바꿔주세요.")
                    elif tagged["grammar_description"][i] == "SINGULAR TO PLURAL VERB":
                        st.write(f"단수형을 복수형으로 바꿔주세요.")
                    elif (
                        tagged["grammar_description"][i]
                        == "SINGULAR VERB TO PAST PARTICIPLE"
                    ):
                        st.write(f"단수형 동사를 과거 분사로 바꿔주세요.")
                    elif (
                        tagged["grammar_description"][i]
                        == "SINGULAR VERB TO PAST TENSE"
                    ):
                        st.write(f"단수형 동사를 과거형으로 바꿔주세요.")
                    elif (
                        tagged["grammar_description"][i]
                        == "SINGULAR VERB TO PRESENT PARTICIPLE"
                    ):
                        st.write(f"단수형 동사를 현재 진행형으로 바꿔주세요.")
                    elif (
                        tagged["grammar_description"][i]
                        == "PAST PARTICIPLE TO PRESENT TENSE"
                    ):
                        st.write(f"시제를 과거 분사에서 현재로 바꿔주세요.")
                    elif (
                        tagged["grammar_description"][i]
                        == "PAST PARTICIPLE TO SINGULAR VERB"
                    ):
                        st.write(f"과거 분사에서 단수형 동사로 바꿔주세요.")
                    elif (
                        tagged["grammar_description"][i]
                        == "PAST PARTICIPLE TO PAST TENSE"
                    ):
                        st.write(f"시제를 과거 분사에서 과거으로 바꿔주세요.")
                    elif (
                        tagged["grammar_description"][i]
                        == "PAST PARTICIPLE TO PRESENT PARTICIPLE"
                    ):
                        st.write(f"시제를 과거 분사에서 현재 진행형으로 바꿔주세요.")
                    elif (
                        tagged["grammar_description"][i]
                        == "PAST TENSE TO PRESENT TENSE"
                    ):
                        st.write(f"시제를 과거에서 현재로 바꿔주세요.")
                    elif (
                        tagged["grammar_description"][i]
                        == "PAST TENSE TO SINGULAR VERB"
                    ):
                        st.write(f"과거형 동사를 단수형으로 동사로 바꿔주세요.")
                    elif (
                        tagged["grammar_description"][i]
                        == "PAST TENSE TO PAST PARTICIPLE"
                    ):
                        st.write(f"시제를 과거에서 과거 분사로 바꿔주세요.")
                    elif (
                        tagged["grammar_description"][i]
                        == "PAST TENSE TO PRESENT PARTICIPLE"
                    ):
                        st.write(f"시제를 과거에서 현재 진행으로 바꿔주세요.")
                    elif (
                        tagged["grammar_description"][i]
                        == "PRESENT PARTICIPLE TO PRESENT TENSE"
                    ):
                        st.write(f"시제를 현재 진행에서 현재로 바꿔주세요.")
                    elif (
                        tagged["grammar_description"][i]
                        == "PRESENT PARTICIPLE TO SINGULAR VERB"
                    ):
                        st.write(f"현재 진행형에서 단수형 동사로 바꿔주세요.")
                    elif (
                        tagged["grammar_description"][i]
                        == "PRESENT PARTICIPLE TO PAST PARTICIPLE"
                    ):
                        st.write(f"시제를 현재 진행에서 과거 분사로 바꿔주세요.")
                    elif (
                        tagged["grammar_description"][i]
                        == "PRESENT PARTICIPLE TO PAST TENSE"
                    ):
                        st.write(f"시제를 현재 진행에서 과거로 바꿔주세요.")
                    elif tagged["grammar_description"][i] == "SINGULAR TO PLURAL NOUN":
                        st.write(f"단수 명사를 복수형으로 바꿔주세요.")
                    elif tagged["grammar_description"][i] == "PLURAL TO SINGULAR NOUN":
                        st.write(f"복수형 명사를 단수형으로 바꿔주세요.")
                    elif tagged["grammar_description"][i] == "PREPOSITION":
                        st.write(
                            f"전치사를 {tagged['ref_word'][i]}에서 {tagged['tag'][i][:8]}으로 바꿔주세요."
                        )
                    elif tagged["grammar_description"][i] == "WRONG USE OF VOCABULARY":
                        if tagged["tag"][i][1] == "R":
                            st.write(
                                f"{tagged['ref_word'][i]}에서 {tagged['tag'][i][9:]}로 바꿔주세요."
                            )
                        elif tagged["tag"][i][1] == "D":
                            st.write(f"{tagged['ref_word'][i]}를 없애주세요.")
                        elif tagged["tag"][i][1] == "A":
                            st.write(
                                f"{tagged['ref_word'][i]} 뒤에 {tagged['tag'][i][:8]} 붙여주세요."
                            )

    else:
        return st.write("틀린 문장이 없네요! 아주 잘 하셨어요.")


def make_layout(question_data):
    by_text, by_speaking = st.tabs(["텍스트", "말하기"])

    with by_text:
        grammar = question_data["grammar"]["phase_2"]
        st.subheader("grammar")
        st.markdown(
            f"전체 발화 문장 중 올바른 문법 사용 비율은 **{grammar['score']}%** 입니다."
        )

        with st.container(height=300):
            st.markdown(grammar["original_passage"])

        fix_sentence(grammar["tag_grammar_info"])

        st.subheader("coherence")
        st.markdown(
            f"- 고객님의 질문에 대한 답변의 주제 적합성은 **{question_data['coherence']}**입니다"
        )
        st.subheader("complexity")
        st.markdown(f"{question_data['complexity']}")

    with by_speaking:
        st.markdown(
            f"전체 발화 중 잘못된 발음 없이 명확하게 발음한 비율은 **{question_data['mpr']}%** 입니다."
        )
        st.markdown(
            f"연속으로 발화한 평균 단어 수는 **{question_data['mlr']}개** 입니다."
        )
        st.markdown(f"전체 발화 중 pause 비율은 **{question_data['pause']}%** 입니다.")


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


response = requests.get(
    url=f"https://mopic.today/api/me/result/{st.session_state['date']}",
    headers={"Access-Token": st.session_state["token"]["access_token"]},
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
questions = requests.get(url="https://mopic.today/api/test").json()

with tab1:
    question_response_1 = requests.get(
        url=f"https://mopic.today/api/me/result/{st.session_state['date']}/1",
        headers={"Access-Token": st.session_state["token"]["access_token"]},
    )

    if question_response_1.status_code == 200:
        question_data_1 = question_response_1.json()

        st.write(f"{question_data_1['q_num']}. {questions['q1']}")

        make_layout(question_data_1)

with tab2:
    question_response_2 = requests.get(
        url=f"https://mopic.today/api/me/result/{st.session_state['date']}/2",
        headers={"Access-Token": st.session_state["token"]["access_token"]},
    )

    if question_response_2.status_code == 200:
        question_data_2 = question_response_2.json()

        st.write(f"{question_data_2['q_num']}. {questions['q2']}")
        make_layout(question_data_2)

with tab3:
    question_response_3 = requests.get(
        url=f"https://mopic.today/api/me/result/{st.session_state['date']}/3",
        headers={"Access-Token": st.session_state["token"]["access_token"]},
    )

    if question_response_3.status_code == 200:
        question_data_3 = question_response_3.json()

        st.write(f"{question_data_3['q_num']}. {questions['q3']}")
        make_layout(question_data_3)
