from datetime import datetime

import requests
import streamlit as st

today: datetime.date = datetime.today()

tested_date = st.date_input("When's your birthday", today)
response = requests.get(
    url=f"https://mopic.today/api/me/result/{tested_date}",
    headers={"access_token": st.session_state["token"]["access_token"]},
)


if response.status_code == 200:
    result = response.json()
    st.session_state["date"] = tested_date
    if st.button("보러가기"):
        st.switch_page("pages/feedback.py")
else:
    st.error("해당 날짜에 응시한 시험이 없습니다.")
    st.session_state["date"] = None
