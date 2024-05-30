import os
import streamlit as st
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv(), override=True)
from openai import OpenAI
llm = ChatOpenAI()
from io import StringIO


# Define the OpenAI API key
openai = OpenAI(
    api_key='key-here',
    base_url="https://api.deepinfra.com/v1/openai",
)

st.title('CODE REFACTORING')
st.divider()

st.text('UPLOAD YOUR FILE or WRITE CODE TO REFACTOR:')
string_data=''
uploaded_file = st.file_uploader("")
if uploaded_file is not None:
    # To convert to a string based IO:
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    # To read file as string:
    string_data = stringio.read()

mycode=st.text_area(label='',placeholder='Write your code here...',value=string_data, height=275,key="code")
option = st.selectbox('SELECT PROGRAMMING LANGUAGE:',('C#', 'Java Script', 'Python','Java','php','c++'))



# Define refactoring rules or guidelines
refactoring_rules = """
1. Red-Green-Refactor: Write a failing test, make it pass, then refactor.
2. Add access modifiers to the class attributes.
3. Add access modifiers to the class functions.
4. Add Comment to every function.
5. Refactoring by abstraction.
6. Simplifying Methods.
7. Moving Features Between Objects.
8. Refactor the code.
"""



# Define cost analysis criteria
cost_analysis_criteria = """
1. Total tokens required to implement the refactoring.
2. Estimated cost in USD to implement the refactoring.
3. Time required to implement the refactoring.
4. Readability improvements.
5. Performance improvements.
"""

def suggest_refactorings(code_snippet,languge):
     print(languge)
     st.markdown(f"**REFACTORING THE CODE SNIPPET IN '{languge}' LANGUAGE**")
     chat_completion  = openai.chat.completions.create(
      model="meta-llama/Llama-2-70b-chat-hf", #meta-llama/Llama-2-7b-chat-hf
        messages=[
            {
            "role": "system",
            "content": "Refactor & Convert the following code snippet in "+ languge+ '.'
            },
            {
            "role": "user",
            "content": code_snippet
            },
            {
            "role": "system",
            "content": "Based on the following refactoring rules:"
            },
            {
            "role": "system",
            "content": refactoring_rules
            },
            {
            "role": "system",
            "content": "Analyze the cost of the refactorings based on the following criteria:"
            },
            {
            "role": "system",
            "content": cost_analysis_criteria
            }
        ],
     max_tokens=1000,
     stream=True,
    )
     return chat_completion

# def refactor_code(code_snippet):
if st.button('REFACTOR CODE'):
    output = ""
    refactorings = suggest_refactorings(mycode,option)
    st.divider()
    st.write_stream(refactorings)

st.divider()
st.markdown('''[:gray[© 2024 Impressico.com, All rights reserved.]](https://www.impressico.com/)''')
