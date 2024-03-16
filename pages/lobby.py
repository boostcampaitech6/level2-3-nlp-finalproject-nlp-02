import streamlit as st

st.subheader("달력을 넣으면 이전 시험 기록 보기를 없애기...")

st.write("{user.name}님, 어서오세요. 지금까지 {user.streak} 연속이에요.")

if st.button("Take a Today's Test"):
    st.switch_page(page="./pages/pretest.py")

if st.button("이전 시험 기록 보기"):
    st.switch_page(page="./pages/history.py")
