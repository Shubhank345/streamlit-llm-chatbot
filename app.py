import streamlit as st
import ollama
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import os 
from dotenv import load_dotenv
load_dotenv()
os.environ['LANGCHAIN_API_KEY']=os.getenv('LANGCHAIN_API_KEY')
os.environ['LANGCHAIN_TRACING_V2'] ='true'
os.environ["LANGCHAIN_PROJECT"] = "Q&A CHATBOT WITH OLLAMA"

prompts =ChatPromptTemplate.from_messages(
    [
        ('system',"You are helpful AI assistant"),
        ('user','Question:{question}')

    ]
)
def generate_response(question,llm,api_key,temperature,max_token):
    llm =ChatOllama(model=llm)
    ollama.api_key=api_key
    parser=StrOutputParser()
    chain=prompts|llm|parser
    answer=chain.invoke({'question':question})
    return answer
#Title of streamlit
st.title("Basic Q&A Chatbot")
#Creating sidebar settings
st.sidebar.title("Settings")
api_key=st.sidebar.text_input("Write your API KEY:",type='password')
llm = st.sidebar.selectbox("Choose your ollama model:",["llama3",'phi3','mistral','gemma:2b'])
temperature=st.slider("Temperature",min_value=0.0,max_value=1.0,value=0.7)
max_token=st.slider('Max_Token',min_value=50,max_value=300,value=150)
#user inteface
st.write("Ask your query")
user_input=st.text_input("You:")
if user_input:
    response=generate_response(user_input,llm,api_key,temperature,max_token)
    st.write(response)
else:
    st.write("No Input Recieved: Please provide your query")