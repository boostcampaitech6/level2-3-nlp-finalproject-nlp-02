import base64
import json

import streamlit as st
import yaml
from streamlit_oauth import OAuth2Component


# load config.yaml
def load_config(filename):
    with open(filename, "r") as config_file:
        config = yaml.safe_load(config_file)
    return config


config = load_config("config.yaml")
google_config = config.get("google")

# create an OAuth2Component instance
CLIENT_ID = google_config.get("client_id")
CLIENT_SECRET = google_config.get("client_secret")
AUTHORIZE_ENDPOINT = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_ENDPOINT = "https://oauth2.googleapis.com/token"
REVOKE_ENDPOINT = "https://oauth2.googleapis.com/revoke"


if "auth" not in st.session_state:
    # create a button to start the OAuth2 flow
    oauth2 = OAuth2Component(
        CLIENT_ID,
        CLIENT_SECRET,
        AUTHORIZE_ENDPOINT,
        TOKEN_ENDPOINT,
        TOKEN_ENDPOINT,
        REVOKE_ENDPOINT,
    )
    result = oauth2.authorize_button(
        name="인증을 위해 한 번 더 클릭해주세요.",
        icon="https://www.google.com.tw/favicon.ico",
        redirect_uri="https://mopic.today/",
        scope="openid email profile",
        key="google",
        extras_params={"prompt": "consent", "access_type": "offline"},
        use_container_width=False,
        pkce="S256",
    )

    if result:
        id_token = result["token"]["id_token"]
        payload = id_token.split(".")[1]
        payload += "=" * (-len(payload) % 4)
        payload = json.loads(base64.b64decode(payload))
        email = payload["email"]
        st.session_state["auth"] = email
        st.session_state["token"] = result["token"]
        st.rerun()

else:
    if st.seeion_state["auth"]:
        st.write(st.seeion_state["auth"])
        if st.button("인증 완료! 다음으로 넘어가주세요."):
            st.switch_page("pages/lobby.py")
    else:
        st.write("인증 실패. 다시 진행해주세요.")
