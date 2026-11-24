import streamlit as st
import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate 

load_dotenv()

# Prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("user", "Question: {question}\nAnswer:")
])

def generate_response(question, api_key, model_name, temperature, max_tokens):
    llm = ChatOpenAI(
        model=model_name,
        openai_api_key=api_key,
        temperature=temperature,
        max_tokens=max_tokens
    )
    chain = prompt | llm | StrOutputParser()
    return chain.invoke({"question": question})

# UI
st.title("Simple Q&A Bot")

st.sidebar.title("Settings")

# ✅ Get env key
env_key = os.getenv("OPENAI_API_KEY")

# ✅ Sidebar input (override)
api_key = st.sidebar.text_input(
    "OpenAI API Key",
    value=env_key if env_key else "",
    type="password"
)

model_name = st.sidebar.selectbox(
    "Model",
    ["gpt-4o", "gpt-4-turbo", "gpt-4"]
)

temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.7)
max_tokens = st.sidebar.slider("Max Tokens", 50, 300, 150)

# Debug (TEMPORARY)
if st.sidebar.checkbox("Show debug info"):
    st.sidebar.write("Env Key Loaded:", bool(env_key))
    st.sidebar.write("API Key Used:", api_key[:10] + "..." if api_key else "None")

user_input = st.text_input("Ask a question:")

if user_input:
    if not api_key:
        st.error("❌ No API key provided")
    else:
        with st.spinner("Thinking..."):
            try:
                answer = generate_response(
                    user_input, api_key, model_name, temperature, max_tokens
                )
                st.success(answer)
            except Exception as e:
                st.error(f"❌ Error: {e}")