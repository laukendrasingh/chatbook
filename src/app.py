import streamlit as st

from pinecone import Pinecone, ServerlessSpec
from helper import display_message, ingest_data
from streamlit_chat import message
from config import *
import logging as log

log.info("START: app")
pc = Pinecone(api_key=PINECONE_API_KEY)

st.title("CHATBOOK")
st.divider()

if st.button('RE-LOAD BOOK DATA', type='primary'):
    with st.spinner(f"Reloading book data..."):
        if any(index.get('name') == INDEX_NAME for index in pc.list_indexes()):
            display_message(f"Deleting index: {INDEX_NAME}")
            pc.delete_index(name=INDEX_NAME)
        display_message(f"Creating index: {INDEX_NAME}")
        pc.create_index(name=INDEX_NAME, dimension=1536, spec=ServerlessSpec(cloud="aws", region=PINECONE_ENV))
        display_message(f"Index: {INDEX_NAME} is created. now re-loading data")
        ingest_data()
        display_message("Book data is successfully re-loaded!")

st.caption('__NOTE:__ It removes the existing index and create new to store data in pinecone DB.')
#Are you sure you want to Delete chatbook-embeddings? Your data will be permanently deleted.
from helper import *

#Create cache
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

if "user_questions" not in st.session_state:
    st.session_state["user_questions"] = []

if "user_answers" not in st.session_state:
    st.session_state["user_answers"] = []

#User interface
st.subheader('CHAT WITH BOOK: HUMAN EVOLUTION')
with st.form(key="QA", clear_on_submit=True):
    prompt = st.text_input(
        "QUESTION",
        placeholder="Enter your question here...",
        key="input_question",
    )
    generate_answer = st.form_submit_button("SUBMIT")


if generate_answer:
    with st.spinner(f"Generating response for: {prompt}"):
        generated_response, cb = get_answer(prompt)
        log.info(cb)
        #Create formatter response
        try:
            sources = set(
                [
                    doc.metadata["source"]
                    for doc in generated_response["source_documents"]
                ]
            )
            formatted_response = (f"{generated_response['answer']} \n\n {create_sources_string(sources)}")
        except:
            formatted_response = f"{generated_response['answer']}"

        #Save question and answers
        st.session_state["user_questions"].insert(0, prompt)
        st.session_state["user_answers"].insert(0,formatted_response)


if st.session_state["user_answers"]:
    for index, (generated_response, user_query) in enumerate(zip(st.session_state["user_answers"], st.session_state["user_questions"],)):
        message(user_query, is_user=True, key=index)
        message(generated_response)

st.divider()
st.markdown('''[:gray[© 2024 Impressico.com, All rights reserved.]](https://www.impressico.com/)''')