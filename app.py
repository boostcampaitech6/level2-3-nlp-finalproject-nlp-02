import streamlit as st

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

login = "http://mopic.today/api/login"

st.title("MOPIc")
st.write("구글 아이디로 로그인하시면 자동으로 회원으로 등록됩니다.")

st.markdown(
    f'<a href="{login}" target="_self" style="display: inline-block; padding: 12px 20px; background-color: lightblue; color: white; text-align: center; text-decoration: none; font-size: 16px; border-radius: 4px;">GOOGLE LOGIN</a>',
    unsafe_allow_html=True,
)
