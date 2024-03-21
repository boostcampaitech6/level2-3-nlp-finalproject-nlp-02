import streamlit as st
import requests
from datetime import datetime

today: datetime.date = datetime.today()

tested_date = st.date_input("시험 본 날을 골라주세요.", today)
response = requests.get(url=f"http://mopic.today/api/me/result/{tested_date}", headers={"access_token": st.session_state['token']['access_token']})


if response.status_code == 200:
    # 응답 데이터 처리 (예: JSON 형태의 응답을 가정)
    result = response.json()
    st.write("응답 데이터:", result)
else:
    st.error("해당 날짜에 응시한 시험이 없습니다.")
