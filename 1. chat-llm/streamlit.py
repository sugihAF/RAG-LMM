import streamlit as st
from streamlit_chat import message
import tempfile
import os

# Import your ChatLLM class.
# (Make sure this file is in the Python path or adjust the import accordingly)
from chatllm import ChatLLM

# Set page title.
st.set_page_config(page_title="Chat with LLM")


def display_messages():
    st.subheader("Chat")
    for i, (msg, is_user) in enumerate(st.session_state["messages"]):
        message(msg, is_user=is_user, key=str(i))
    st.session_state["thinking_spinner"] = st.empty()

def process_input():
    # Process the user input if it exists and is not just whitespace.
    if st.session_state["user_input"] and st.session_state["user_input"].strip():
        user_text = st.session_state["user_input"].strip()
        with st.session_state["thinking_spinner"], st.spinner("Thinking..."):
            # Get the response from the assistant.
            agent_text = st.session_state["assistant"].ask(user_text)

        # Append the user and agent messages to the session.
        st.session_state["messages"].append((user_text, True))
        st.session_state["messages"].append((agent_text, False))
        # Clear the text input value.
        st.session_state["user_input"] = ""

def page():
    # Initialize session state variables if they don't exist.
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
    if "assistant" not in st.session_state:
        st.session_state["assistant"] = ChatLLM()  # Instantiate your chat LLM.

    st.header("Chat with LLM")

    st.divider()
    # Display chat conversation.
    display_messages()
    
    # Input text for user message.
    st.text_input("Message", key="user_input", on_change=process_input)

if __name__ == "__main__":
    page()
