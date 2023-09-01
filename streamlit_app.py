import streamlit as st
from BackEnd.FireBaseDB.access_db import auth
from respond_query import get_response
from lang_tranlsator import translate_to_lang


# App title
st.set_page_config(page_title="🤖🏦 BotMora")
st.session_state.token = None

# Replicate Credentials
with st.sidebar:
    # st.title("🤖🏦 BotMora")
    st.markdown("<h1 style='text-align: center; font-size:40px;'>🤖🏦 BotMora</h1>", unsafe_allow_html=True)

    st.markdown("***")
    # st.text("")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    col1, col2, col3 = st.columns((2, 2, 2))

    if username and password:
        try:
            token = auth.sign_in_with_email_and_password(username, password)
            if token:
                st.session_state.token = token
        except:
            token = None

    if col2.button("Login"):
        if username and password:
            # Authenticate the user
            # token = replicate.LoginWithCredentials(username, password)
            try:
                token = auth.sign_in_with_email_and_password(username, password)
                if token:
                    st.session_state.token = token
            except:
                token = None
            
            if st.session_state.token:
                st.success("Login successful.", icon="✅")
                
                col11, col21, col31 = st.sidebar.columns((2, 2, 2))
                if col21.button("Logout"):
                    # Remove the token from the Streamlit session state
                    del st.session_state.token
                    st.success("Logout successful.")
            else:
                st.error("ERROR: Invalid username or password.")
        else:
            st.error("ERROR: Please enter both username and password.")

    if "REPLICATE_API_TOKEN" in st.secrets:
        st.success("API key already provided!", icon="✅")
        replicate_api = st.secrets["REPLICATE_API_TOKEN"]
    else:
        replicate_api = st.text_input("Enter Replicate API token:", type="password")
        if not (replicate_api.startswith("r8_") and len(replicate_api) == 40):
            st.warning("Please enter your credentials!", icon="⚠️")
        else:
            st.success("Proceed to entering your prompt message!", icon="👉")
    
    selected_language = st.sidebar.selectbox(
        "Select the preferred language",
        ["English", "Tamil", "Sinhala"],
        key="selected_language",
    )
    if selected_language == "Tamil":
        lang = "ta"
    elif selected_language == "Sinhala":
        lang = "si"
    else:
        lang = "en"

# Store LLM generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [
        {"role": "assistant", "content": "How may I assist you today?", "translated": translate_to_lang("How may I assist you today?", "en", lang)}
    ]

# Display or clear chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if "translated" in message.keys():
            st.write(message["translated"])
        else:
            st.write(message["content"])


def clear_chat_history():
    st.session_state.messages = [
        {"role": "assistant", "content": "How may I assist you today?"}
    ]


col1, col2, col3 = st.sidebar.columns((0.5, 2, 0.5))
col2.button("Clear Chat History", on_click=clear_chat_history)

def get_assistant_response(prompt_input):
    output, eng_response = get_response(
        prompt_input,
        st.session_state.messages,
        token=st.session_state.token,
        translate_to=lang,
    )
    return output, eng_response


# User-provided prompt
if prompt := st.chat_input(disabled=(not replicate_api) or (not st.session_state.token)):
    translated_user_input = translate_to_lang(prompt, lang, "en")
    st.session_state.messages.append({"role": "user", "content": translated_user_input, "translated": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response, eng_response = get_assistant_response(translated_user_input)
            placeholder = st.empty()
            placeholder.markdown(response)
    message = {"role": "assistant", "content": eng_response, "translated": response}
    st.session_state.messages.append(message)