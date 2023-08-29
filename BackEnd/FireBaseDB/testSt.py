import streamlit as st
from Test import LoginWithCredentials,GetAccountWithToken

# Create a Streamlit sidebar for logging
# st.sidebar.title("Logging")

# Create a text area to display logs
log_output = st.empty()

# Function to log messages
def log_message(message):
    log_output.text(message)

# Username and Password Input
username = st.text_input("Username")
password = st.text_input("Password", type="password")

# Login Button
if st.button("Login"):
    if username and password:
        # Authenticate the user
        token = LoginWithCredentials(username, password)
        if token:
            # Store the token in the Streamlit session state
            st.session_state.token = token
            log_message("Login successful.")
            if st.button("Logout"):
                # Remove the token from the Streamlit session state
                del st.session_state.token
                log_message("Logout successful.")
        else:
            log_message("ERROR: Invalid username or password.")
    else:
        log_message("ERROR: Please enter both username and password.")
