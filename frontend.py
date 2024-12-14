import streamlit as st
from datetime import datetime
from llm_calls import answer_question
from streamlit_float import *
from PIL import Image
from utility import handle_pdf_ingestion_tempfile
import json

st.set_page_config(
    page_title="🤖 Chat with LLM",
    layout = "centered"
)
if "messages" not in st.session_state:
    st.session_state.messages = []

if "current_downloads" not in st.session_state:
    st.session_state.current_downloads = []

if "document_uploaded" not in st.session_state:
    st.session_state.document_uploaded = []

float_init()
st.subheader("🤖 Chat with LLM")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

with st.sidebar:
    st.markdown("📃 Chat with Document")
    uploaded_file = st.file_uploader(
        label="Upload Image", 
        label_visibility='collapsed',
        key="image_uploader"
    )
    if uploaded_file:
        res = handle_pdf_ingestion_tempfile(uploaded_file)
        print(res)
        if res:
            st.session_state.document_uploaded.append(uploaded_file)
            st.write("sucessfully uploaded")
        else:
            st.write("upload failed")

    if st.button("🧹 clear all"):
        if "messages" in st.session_state:
            st.session_state["messages"] = []
        if "conversation_id" in st.session_state:
            del st.session_state["conversation_id"]
        if "document_uploaded" in st.session_state:
            st.session_state["document_uploaded"] = []
        st.rerun()

if prompt := st.chat_input("Ask an question or generate an image..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    query = {"query": prompt}
    with st.chat_message("assistant"):
        try:
            with st.spinner("generating...please for it.."):
                response = None
                if (len(st.session_state.document_uploaded) > 1):
                    response = answer_question(query["query"], documet_count_inmenory = True)
                else:
                    response = answer_question(query["query"], documet_count_inmenory = False)
                answer = response.answer
                if response.document_path != "":
                    img_path = response.document_path
                    image = Image.open(img_path)
                    st.image(image)
                st.markdown(answer)                  
        except ValueError as e:
            st.error(f"Error: {e}")
        print(">>>>>>", answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})


def log_feedback(icon):
    st.toast("Thanks for your feedback!", icon="👌")
    last_messages = json.dumps(st.session_state["messages"][-2:])
    activity = datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ": "
    activity += "positive" if icon == "👍" else "negative"
    activity += ": " + last_messages


if len(st.session_state["messages"]) > 0:
    if "conversation_id" not in st.session_state:
        st.session_state["conversation_id"] = "history_" + datetime.now().strftime("%Y%m%d%H%M%S")

    action_buttons_container = st.container()
    action_buttons_container.markdown(
        """
        <style>
        .floating-container {
            position: fixed;
            bottom: 7.2rem;
            background-color: var(--default-backgroundColor);
            padding-top: 1rem;
            width: 100%;
            z-index: 1000;
        }
        </style>
        """, 
        unsafe_allow_html=True
    )

    cols_dimensions = [9, 9, 100 - sum([9, 9])]
    col1, col2, _ = action_buttons_container.columns(cols_dimensions)

    with col1:
        icon = "👍"
        if st.button(icon):
            log_feedback(icon)

    with col2:
        icon = "👎"
        if st.button(icon):
            log_feedback(icon)