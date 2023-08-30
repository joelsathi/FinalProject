import streamlit as st
import replicate
import os

import sys
sys.path.append("C:\\University\\Academics_5th_sem\\7. Data Science & Engineering Project\\FinalProject\\BackEnd\\LLM\\llm_out.py")
sys.path.append("C:\\University\\Academics_5th_sem\\7. Data Science & Engineering Project\\FinalProject\\respond_query.py")
# sys.path.append("C:\\University\\Academics_5th_sem\\7. Data Science & Engineering Project\\FinalProject\\BackEnd\\repond_query.py")
from BackEnd.LLM.llm_out import get_output_llm

from respond_query import get_response

# App title
st.set_page_config(page_title="🤖🏦 BotMora")

# Replicate Credentials
with st.sidebar:
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username and password:
            # Authenticate the user
            token = replicate.LoginWithCredentials(username, password)
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
    st.title('🤖🏦 BotMora')
    if 'REPLICATE_API_TOKEN' in st.secrets:
        st.success('API key already provided!', icon='✅')
        replicate_api = st.secrets['REPLICATE_API_TOKEN']
    else:
        replicate_api = st.text_input('Enter Replicate API token:', type='password')
        if not (replicate_api.startswith('r8_') and len(replicate_api)==40):
            st.warning('Please enter your credentials!', icon='⚠️')
        else:
            st.success('Proceed to entering your prompt message!', icon='👉')

# Store LLM generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

# Display or clear chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]
st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

user_msgs = []
assistant_msgs = ["Assistant: How may I assist you today?"]

dialogue = "Assistant: How may I assist you today?"


def get_assistant_response(prompt_input):
    output = get_response(prompt_input, st.session_state.messages)
    return output

# Function for generating LLaMA2 response
def generate_llama2_response(prompt_input, context="", db_ans=""):

    answer_using_context_template = """
                                    {chat_history}
                                    User: {user_msg}
                                    You should use the following context to answer the question
                                    Context: {context}
                                    Finish the Answer as the assistant:
                                    Assistant:
                                    """
    
    answer_using_database_answer_template = """
                                    {chat_history}
                                    User: {user_msg}
                                    The following context is provided to you to answer the question
                                    Context: {db_ans}
                                    Formulate the answer using the context provided and answer the question as the assistant:
                                    Assistant:
                                    """
    
    answer_using_llm = """
                        {chat_history}
                        User: {user_msg}
                        You should only answer this question if this question is in the banking domain as the assistant.
                        If this question is not in the banking domain, you should reply, 'I am a banking chatbot, I am not trained to answer this question.', and you should not provide information more on that subject.
                        Assistant:
                        """

    l = len(st.session_state.messages)
    cnt = 0
    chat_history = ""
    for dict_message in st.session_state.messages:
        if dict_message["role"] == "user":
            if l - cnt <= 6:
                chat_history += "User: " + dict_message["content"] + "\n\n"
        else:
            if l - cnt <= 6:
                chat_history += "Assistant: " + dict_message["content"] + "\n\n"
        cnt += 1
    
    if context != "":
        string_dialogue = answer_using_context_template.format(chat_history=chat_history, user_msg=prompt_input, context=context)
    elif db_ans != "":
        string_dialogue = answer_using_database_answer_template.format(chat_history=chat_history, user_msg=prompt_input, db_ans=db_ans)
    else:
        string_dialogue = answer_using_llm.format(chat_history=chat_history, user_msg=prompt_input)

    output = get_output_llm(prompt=string_dialogue)

    return output

# User-provided prompt
if prompt := st.chat_input(disabled=not replicate_api):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = get_assistant_response(prompt)
            placeholder = st.empty()
            full_response = ''
            for item in response:
                full_response += item
                placeholder.markdown(full_response)
            placeholder.markdown(full_response)
    message = {"role": "assistant", "content": full_response}
    st.session_state.messages.append(message)
