import streamlit as st
import requests


API_URL = "http://127.0.0.1:8000/chat"
USER_ID = "bob123" # can be dynamic later

st.set_page_config(page_title="AI ChatBot with Memory ",
                   page_icon="🤖", layout= "centered")
st.title("Chat with your PDF and Memory and web search")
st.markdown("Chat with local LLM that remembers your conversation.")

# Initialize Session state
if "messages" not in st.session_state:
    st.session_state["messages"]=[]
# web search toggle
use_web = st.sidebar.checkbox("🌐Enable web search")

# Upload PDF
upload_file = st.file_uploader("Upload your PDF", type = ["pdf"])
if upload_file is not None:
    files = {"file": upload_file.getvalue()}
    res = requests.post(f"{API_URL}/upload_pdf", params={"user_id": USER_ID}, files={"file":upload_file})
    if res.status_code == 200:
        st.success("PDF uploaded and processed")

# Display chat history
for role, message in st.session_state["messages"]:
    with st.chat_message(role):
        st.markdown(message)
# user input
if prompt :=st.chat_input("Ask a question..."):
    #add user message to chat history
    st.session_state["messages"].append(("user", prompt))
    with st.chat_message("user"):
        st.markdown(prompt)

    # send to backend
    params = {"use_web": str(use_web).lower()}
    payload = {"user_id": USER_ID, "message": prompt, "use_web":use_web}
    res = requests.post(API_URL, json=payload)

    if res.status_code == 200:
        bot_message = res.json()["response"]
    else:
        bot_message = "Error: Could not connect to Backend"
    # Display Assistance Response
    st.session_state["messages"].append(("assistant",bot_message))
    with st.chat_message("assistant"):
        st.markdown(bot_message)