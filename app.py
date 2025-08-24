# app.py
import streamlit as st
import requests
import uuid
import time

st.set_page_config(page_title="Ezz ChatBot", page_icon="🤖", layout="centered")

st.markdown("<h1 style='text-align: center;'>🤖 Ezz ChatBot</h1>", unsafe_allow_html=True)

# Session ID
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# Messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("Say something to Ezz..."):
    # Show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Placeholder for bot
    with st.chat_message("assistant"):
        placeholder = st.empty()
        placeholder.markdown("Ezz is thinking...")

        try:
            # Call FastAPI backend
            response = requests.post(
                "http://127.0.0.1:8000/chat",
                json={"prompt": prompt, "session_id": st.session_state.session_id}
            )

            if response.status_code == 200:
                answer = response.json()["answer"]
            else:
                answer = "❌ Error from API"
        except Exception as e:
            answer = f"⚠️ Could not connect to API: {e}"

        time.sleep(1)
        placeholder.markdown(answer)

    # Save bot response
    st.session_state.messages.append({"role": "assistant", "content": answer})
