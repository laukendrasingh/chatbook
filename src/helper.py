import time
import streamlit as st

from langchain.vectorstores import Pinecone
from langchain.embeddings import OpenAIEmbeddings
from typing import Set
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.callbacks import get_openai_callback
from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from config import *
import logging as log

# Function to put test-book embaddings in pinecone vector db
def ingest_data():
    log.info('********** START: ingest data **********')
    loader = DirectoryLoader("data/book", glob="**/*.txt")
    raw_data = loader.load()
    log.info(f"Loaded {len(raw_data) } data")

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=10)
    data = text_splitter.split_documents(documents=raw_data)
    log.info(f"Splitted into {len(data)} chunks. now going to add to pinecone")

    embeddings = OpenAIEmbeddings()
    Pinecone.from_documents(data, embeddings, index_name=INDEX_NAME)

    log.info('********** END: ingest data **********')


def display_message(message, duration=1):
    log.info(message)
    st.toast(message)
    time.sleep(duration)


def get_pinecone_retriever():
    return Pinecone.from_existing_index(index_name=INDEX_NAME, embedding=OpenAIEmbeddings())


def create_sources_string(source_urls: Set[str]) -> str:
    if not source_urls:
        return ""
    sources_list = list(source_urls)
    sources_list.sort()
    sources_string = "sources:\n"
    for i, source in enumerate(sources_list):
        sources_string += f"{i+1}. {source}\n"
    return sources_string


def add_in_memory(question, answer):
     st.session_state['chat_history'].append((question, answer))


def get_answer(question):
    llm = ChatOpenAI(verbose=LLM_VERBOSE)
    chain = ConversationalRetrievalChain.from_llm(
                    llm=llm,
                    chain_type="stuff",
                    retriever=get_pinecone_retriever().as_retriever(),
                    return_source_documents=True,
                )
    
    with get_openai_callback() as cb:
      result = chain({"question": question, "chat_history": st.session_state['chat_history']})
      add_in_memory(question, result["answer"])
    return result, cb
