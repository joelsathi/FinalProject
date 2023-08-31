import streamlit as st
import replicate
import os

import sys
sys.path.append("C:\\University\\Academics_5th_sem\\7. Data Science & Engineering Project\\FinalProject\\BackEnd\\LLM\\llm_out.py")
sys.path.append("C:\\University\\Academics_5th_sem\\7. Data Science & Engineering Project\\FinalProject\\respond_query.py")
# sys.path.append("C:\\University\\Academics_5th_sem\\7. Data Science & Engineering Project\\FinalProject\\BackEnd\\repond_query.py")
from BackEnd.LLM.llm_out import get_output_llm
from BackEnd.FireBaseDB.access_db import auth

from respond_query import get_response

# App title
st.set_page_config(page_title="🤖🏦 BotMora")

# Replicate Credentials
with st.sidebar:
    st.title('🤖🏦 BotMora')

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username and password:
            # Authenticate the user
            # token = replicate.LoginWithCredentials(username, password)
            try:
                token = auth.sign_in_with_email_and_password(username, password)
            except:
                token = None
                
            if token:
                # Store the token in the Streamlit session state
                st.session_state.token = token
                st.success("Login successful.")
                if st.button("Logout"):
                    # Remove the token from the Streamlit session state
                    del st.session_state.token
                    st.success("Logout successful.")
            else:
                st.error("ERROR: Invalid username or password.")
        else:
            st.error("ERROR: Please enter both username and password.")
    
    if 'REPLICATE_API_TOKEN' in st.secrets:
        st.success('API key already provided!', icon='✅')
        replicate_api = st.secrets['REPLICATE_API_TOKEN']
    else:
        replicate_api = st.text_input('Enter Replicate API token:', type='password')
        if not (replicate_api.startswith('r8_') and len(replicate_api)==40):
            st.warning('Please enter your credentials!', icon='⚠️')
        else:
            st.success('Proceed to entering your prompt message!', icon='👉')
    
    selected_language = st.sidebar.selectbox('Select the preferred language', ['English', 'Tamil', 'Sinhala'], key='selected_language')
    if selected_language == 'Tamil':
        lang = 'ta'
    elif selected_language == 'Sinhala':
        lang = 'si'
    else:
        lang = 'en'

# Store LLM generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

# Display or clear chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if "translated" in message.keys():
            st.write(message["translated"])
        else:
            st.write(message["content"])

def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]
st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

user_msgs = []
assistant_msgs = ["Assistant: How may I assist you today?"]

dialogue = "Assistant: How may I assist you today?"


def get_assistant_response(prompt_input):
    output, eng_response = get_response(prompt_input, st.session_state.messages, token=token, translate_to=lang)
    return output, eng_response

# User-provided prompt
if prompt := st.chat_input(disabled=not replicate_api):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response, eng_response = get_assistant_response(prompt,token=st.session_state.token)
            placeholder = st.empty()
            placeholder.markdown(response)
    message = {"role": "assistant", "content": eng_response, "translated": response}
    st.session_state.messages.append(message)
