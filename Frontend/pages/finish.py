import streamlit as st

st.write("시험이 모두 종료되었습니다!")
st.write("약 2분 정도 뒤에 결과를 확인할 수 있습니다.")
st.write("로비에서 메인 페이지를 확인해주세요.")

if st.button("로비로 돌아가기."):
    st.switch_page("pages/lobby.py")