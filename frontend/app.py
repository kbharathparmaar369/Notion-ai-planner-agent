
import streamlit as st
import requests
import uuid
import os

st.set_page_config(page_title="Notion AI Planner")

st.title("Notion AI Planner")
st.caption("Ask me to plan your day , check tasks , or check the weather")

backend_url = os.getenv("BACKEND_URL", "http://127.0.0.1:8000/chat")

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# this is to keep the chat in the session state so they show up on screen
if "messages" not in st.session_state:
    st.session_state.messages = []


with st.sidebar:
    st.subheader("Try Asking")
    st.write("Plan my day , I am in Bengaluru")
    st.write("what tasks do i have ?")
    st.write("create a task called  'call mom ' for tomorrow")
    st.write("what is the weather right now ?")

    if st.button("clear chat"):
        st.session_state.messages = []
        st.session_state.session_id = str(uuid.uuid4())
        st.rerun()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

user_input= st.chat_input("type your message..")

if user_input:
    st.session_state.messages.append({"role":"user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)
    
    with st.chat_message("assistant"):
        with st.spinner("Thinking .."):
            try:
                response = requests.post(
                    backend_url,
                    json = {
                            "message" : user_input,
                            "session_id" : st.session_state.session_id,
                    },
                    timeout=60,
                )
                response.raise_for_status()
                reply = response.json()["reply"]
            except requests.exceptions.RequestException as e:
                reply = "Something went wrong talking to the backend : " + str(e)
            
            st.write(reply)
    
    st.session_state.messages.append({"role": "assistant", "content" : reply})