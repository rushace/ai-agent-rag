# frontend/app.py


import sys
from pathlib import Path

# Fix: Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

import streamlit as st
import requests
import uuid
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Advocate Assistant", page_icon="⚖️", layout="wide")

st.title("⚖️ Advocate Assistant")
st.caption("Phase 1: Enhanced Legal Chat Assistant | English + Hindi")

# Session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("Enter your Legal Query Here: "):
    # Add user message to UI
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Call backend
    with st.chat_message("assistant"):
        with st.spinner("Advocate Assistant thinking..."):
            try:
                response = requests.post(
                    "http://localhost:8000/chat",
                    json={
                        "message": prompt,
                        "session_id": st.session_state.session_id
                    },
                    timeout=60
                )
                response.raise_for_status()
                data = response.json()

                assistant_reply = data["response"]
                st.markdown(assistant_reply)

                # Save to history
                st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
            except Exception as e:
                st.error(f"Error: {str(e)}")

# Sidebar
with st.sidebar:
    st.header("Phase 1 - Enhanced Legal Chat ✅")
    st.info("• Conversation memory added\n• Better legal prompt\n• ")
    
    if st.button("Clear Conversation"):
        # Clear frontend
        st.session_state.messages = []
        # Clear backend memory
        try:
            requests.post(f"http://localhost:8000/clear-session/{st.session_state.session_id}")
        except:
            pass
        st.session_state.session_id = str(uuid.uuid4())
        st.rerun()

    # st.caption("Tip: Try asking in Hindi for better results.")