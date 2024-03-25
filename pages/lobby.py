import requests
import streamlit as st

st.markdown("""
    <style>
        section[data-testid="stSidebar"][aria-expanded="true"]{
            display: none;
        }
    </style>
    """, unsafe_allow_html=True)

response = requests.post(
    "http://mopic.today/api/get-me",
    json={"token": st.session_state["token"]["access_token"]},
)

# response 예제
# {
#     "sub":"00..123456789...00"
#     "name":"full name"
#     "given_name":"given_name"
#     "family_name":"family_name"
#     "picture":"https://lh3.googleusercontent.com/a/ ... "
#     "email":"example@gmail.com"
#     "email_verified":true
#     "locale":"en"
# }

if response.status_code == 200:
    user_info = response.json()
    user_name = user_info.get("name", "Unknown")
    user_streak = user_info.get("streak", 0)

    st.write(f"{user_name}님, 어서오세요. 지금까지 {user_streak} 연속이에요.")
else:
    st.error("서버로부터 사용자 정보를 가져오는데 실패했습니다.")

if st.button("Take a Today's Test"):
    st.switch_page(page="./pages/pretest.py")

if st.button("이전 시험 기록 보기"):
    st.switch_page(page="./pages/history.py")
