import streamlit as st
from respond_query import get_response
from lang_translator import translate_to_lang

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
    
    selected_language = st.sidebar.selectbox('Select the preferred language', ['Tamil', 'Sinhala', 'English'], key='selected_language')
    if selected_language == 'Tamil':
        lang = 'ta'
    elif selected_language == 'Sinhala':
        lang = 'si'
    else:
        lang = 'en'

# Store LLM generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?", "translated_res": "How may I assist you today?"}]

# Display or clear chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if "translated_res" in message:
            st.write(message["translated_res"])
        else:
            st.write(message['content'])

def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]
st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

def get_assistant_response(prompt_input):
    output, eng_res = get_response(prompt_input, st.session_state.messages, translate_to=lang)
    return output, eng_res

# User-provided prompt
if prompt := st.chat_input(disabled=not replicate_api):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response, eng_res = get_assistant_response(prompt)
            placeholder = st.empty()
            # full_response = ''
            # for item in response:
            #     full_response += item
            #     placeholder.markdown(full_response)
            placeholder.markdown(response)
    message = {"role": "assistant", "content": eng_res, "translated_res": response}
    st.session_state.messages.append(message)
