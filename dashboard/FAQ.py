import streamlit as st
import json
import pyrebase

firebaseConfig = {
    "apiKey": "AIzaSyDTrPMLJ9PnNqPPiY4KETnMAkNXSDVf1iM",
    "authDomain": "botmora-25373.firebaseapp.com",
    "databaseURL": "https://botmora-25373-default-rtdb.firebaseio.com",
    "projectId": "botmora-25373",
    "storageBucket": "botmora-25373.appspot.com",
    "messagingSenderId": "223313770308",
    "appId": "1:223313770308:web:bdb2bb2e428ddf11a70911",
    "measurementId": "G-ZPYWSE9S0J",
}

firebase = pyrebase.initialize_app(firebaseConfig)
pyrebase_db = firebase.database()


def get_top_FAQ_intents(limit=5):
    try:
        # Retrieve all FAQ intents and their data
        faq_intents = pyrebase_db.child("FAQ").get()

        if faq_intents is not None:
            faq_data = faq_intents.val()
            if faq_data:
                # Sort the FAQ intents by count in descending order
                sorted_faq_intents = sorted(
                    faq_data.items(), key=lambda x: x[1]["count"], reverse=True
                )
                # Get the top FAQ intents
                top_intents = sorted_faq_intents[:limit]
                # Create a JSON object with the top 5 intents
                top_json = {}
                for intent, data in top_intents:
                    top_json[intent] = data
                return json.dumps(top_json)
            else:
                return json.dumps({})
    except Exception as e:
        print(f"Error: {e}")
        return json.dumps({"error": str(e)})


# Streamlit app
def main():
    st.title("Top 5 Frequently Asked Questions")

    # Get the top 5 FAQ intents and convert the JSON string to a dictionary
    top_intents = json.loads(get_top_FAQ_intents())

    if not top_intents:
        st.warning("No FAQ data available.")
    else:
        st.write("Top 5 FAQs:")

        for index, (intent, data) in enumerate(top_intents.items(), start=1):
            st.subheader(f"#{index}: {intent}")
            st.write("Count:", data["count"])
            st.write("Question:", data["question"])
            st.markdown("---")


if __name__ == "__main__":
    main()
