import requests
import streamlit as st

test = "http://223.130.130.161:8888/api/test"

qlist = requests.get(url=test)
st.write(qlist.json())