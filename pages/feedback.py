import streamlit as st

st.title("Daily Test \n")

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
    '당신의 예상 등급은 <span class="score">{final.socre}</span> 입니다.', unsafe_allow_html=True
)

tab1, tab2, tab3 = st.tabs(["1번", "2번", "3번"])
# TODO: 해당 시험의 날짜를 받아오도록 함수 변경

with tab1:
    # requests.get(url=test)
    st.header("{question[q1]}")

    # TODO: 저장된 결과에 문제 번호 별로 받아오는 함수 생성

    # response = requests.get(url=result, files=files)
    # if response.status_code == 200:
    #     data = response.json()
    #     st.write(data)

with tab2:
    st.header("질문2")

with tab3:
    st.header("질문3")