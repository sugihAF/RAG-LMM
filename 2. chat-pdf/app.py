# app.py
import os
import base64
import gc
import uuid
import tempfile

import streamlit as st

from chatRAG import build_query_engine  # import backend functions

# Initialize session state variables if not already set
if "id" not in st.session_state:
    st.session_state.id = uuid.uuid4()
if "file_cache" not in st.session_state:
    st.session_state.file_cache = {}
if "messages" not in st.session_state:
    st.session_state.messages = []
if "uploaded_file_bytes" not in st.session_state:
    st.session_state.uploaded_file_bytes = None  # will store bytes of the uploaded file
if "uploaded_file_name" not in st.session_state:
    st.session_state.uploaded_file_name = None  # will store the filename

session_id = st.session_state.id

def reset_chat():
    st.session_state.messages = []
    gc.collect()

def display_pdf(file_bytes):
    """
    Display the uploaded PDF in an iframe.
    """
    st.markdown("### PDF Preview")
    base64_pdf = base64.b64encode(file_bytes).decode("utf-8")
    pdf_display = (
        f'<iframe src="data:application/pdf;base64,{base64_pdf}" '
        'width="400" height="100%" type="application/pdf" '
        'style="height:100vh; width:100%"></iframe>'
    )
    st.markdown(pdf_display, unsafe_allow_html=True)

# Sidebar: File Upload and Document Indexing
with st.sidebar:
    st.header("Add your documents!")

    # Allow file upload (if file exists in session state, recreate a BytesIO-like object)
    uploaded_file = st.file_uploader("Choose your `.pdf` file", type="pdf")

    if uploaded_file is not None:
        # Save the uploaded file bytes and filename to session_state
        file_bytes = uploaded_file.getvalue()
        st.session_state.uploaded_file_bytes = file_bytes
        st.session_state.uploaded_file_name = uploaded_file.name

        file_key = f"{session_id}-{uploaded_file.name}"
        st.write("Indexing your document...")
        if file_key not in st.session_state.file_cache:
            try:
                # Reconstruct a file-like object using the stored bytes (if needed)
                # Here we pass the original file-like object, but you could also wrap the bytes
                # using io.BytesIO(file_bytes) if the backend expects that.
                query_engine = build_query_engine(uploaded_file, session_id)
                st.session_state.file_cache[file_key] = query_engine
                st.success("Ready to Chat!")
            except Exception as e:
                st.error(f"An error occurred while processing the document: {e}")
                st.stop()
        else:
            query_engine = st.session_state.file_cache[file_key]

        # Always display the PDF preview once the file has been uploaded.
        display_pdf(file_bytes)

    # Else, if there is no file in the uploader but one is stored, display the PDF preview.
    elif st.session_state.uploaded_file_bytes is not None:
        st.markdown("### Your Document")
        display_pdf(st.session_state.uploaded_file_bytes)

# Main Chat Interface Layout
col1, col2 = st.columns([6, 1])

with col1:
    logo_path = "./DEEPSEEK.png"
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as image_file:
            logo_b64 = base64.b64encode(image_file.read()).decode()
        st.markdown(
            f"""
            # Chat with your PDF with RAG powered by <img src="data:image/png;base64,{logo_b64}" width="150" style="vertical-align: -3px;">
            """,
            unsafe_allow_html=True,
        )
    else:
        st.header("RAG Chat")

with col2:
    st.button("Clear ↺", on_click=reset_chat)

# Display chat messages history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user chat input and display streaming response
if prompt := st.chat_input("What's up?"):
    # Append user's message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Show assistant's response using a placeholder for streaming responses
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        # Retrieve the query engine from file_cache.
        # We use the stored uploaded file name to recreate the key.
        file_name = st.session_state.get("uploaded_file_name")
        if file_name:
            file_key = f"{session_id}-{file_name}"
            query_engine = st.session_state.file_cache.get(file_key)
        else:
            query_engine = None

        if not query_engine:
            st.error("No document available. Please upload a PDF in the sidebar.")
            st.stop()

        # Query the engine with streaming enabled.
        streaming_response = query_engine.query(prompt)

        # Stream the response chunks in real time.
        for chunk in streaming_response.response_gen:
            full_response += chunk
            message_placeholder.markdown(full_response + "▌")

        message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
