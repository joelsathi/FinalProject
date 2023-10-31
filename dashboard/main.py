import streamlit as st
import pyrebase
import json
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px

# Firebase configuration
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
auth = firebase.auth()

data = pyrebase_db.child("intent").get().val()

# Create a list of dictionaries with the desired structure
intent_data_list = [
    {
        "Intent": intent,
        "Positive": intent_data["positive"],
        "Negative": intent_data["negative"],
    }
    for intent, intent_data in data.items()
]


# Function to retrieve the top FAQ intents
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
                # Create a JSON object with the top intents
                top_json = {}
                for intent, data in top_intents:
                    top_json[intent] = data
                return top_json
            else:
                return {}
    except Exception as e:
        return {"error": str(e)}


# Streamlit app
def main():
    # Define zero margin to occupy the entire browser screen
    app_margin = "0"  # Set the margin to 0 to occupy the whole screen

    # Apply CSS styles to the entire app to remove margins
    st.markdown(
        f"""
        <style>
            .stApp {{
                margin: {app_margin};
            }}
        </style>
    """,
        unsafe_allow_html=True,
    )
    # Add a title with a line underneath for "Admin Dashboard"
    st.markdown(
        "<h1 style='text-align: center; font-size: 60px; border-bottom: 1px solid #ccc;'>Admin Dashboard</h1>",
        unsafe_allow_html=True,
    )

    df_intent = pd.DataFrame(intent_data_list)

    # Create an interactive clustered bar chart using Plotly
    fig = px.bar(
        df_intent,
        x="Intent",
        y=["Positive", "Negative"],
        labels={"value": "Counts"},
        color_discrete_map={"Positive": "palegreen", "Negative": "lightcoral"},
    )

    # Add hover text to display count values
    fig.update_traces(
        hovertemplate='<span style="font-size: 14px; color: black;"> %{x}: %{y} units</span>',
    )

    # Customize layout
    fig.update_layout(
        xaxis_title="Intents",
        yaxis_title="Counts",
        barmode="group",
    )

    time_data = pyrebase_db.child("Time_stamp").get().val()

    # Assuming time_data is a list of dictionaries with days and other keys
    days = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]
    day_data = {}

    # add the week days and counts of them into the new dictionary
    for day in days:
        day_data[day] = time_data[day].get("count")

    # Create a list of dictionaries with the desired structure
    day_data_list = [
        {
            "Day": day,
            "Count": intent_data,
        }
        for day, intent_data in day_data.items()
    ]

    df_day = pd.DataFrame(day_data_list)
    # Create an interactive clustered bar chart using Plotly
    fig_day = px.bar(
        df_day,
        x="Day",
        y=["Count"],
        color="Day",
        labels={"value": "Counts"},
        # color_discrete_map={"Positive": "palegreen", "Negative": "lightcoral"},
    )

    hours = list(range(1, 25))
    hour_data = {}

    # add the week days and counts of them into the new dictionary
    for hour in hours:
        hour_data[str(hour)] = time_data[str(hour)].get("count")

    hour_data_list = [
        {
            "Hour": hour,
            "Count": intent_data,
        }
        for hour, intent_data in hour_data.items()
    ]

    df_hour = pd.DataFrame(hour_data_list)

    # Create an interactive clustered bar chart using Plotly
    fig_hour = px.pie(
        df_hour,
        values="Count",
        names="Hour",
        title="Hour Wise Count",
        # color_discrete_map={"Positive": "palegreen", "Negative": "lightcoral"},
    )

    # Create two columns
    col1, col2 = st.columns(2)

    with col1:
        st.title("Sentiment Analysis of Queries")
        # Use the data from the merged code

        # Display the interactive chart in the first column
        col1.plotly_chart(fig, use_container_width=True)

    with col2:
        st.title("Time Analysis of Queries")
        # # Create a radio button selection for day and hour
        # selection = st.select_slider("Select Option", options=["Day", "Hour"])

        # Create a column with a specific width
        slider_col = st.columns(8)
        # Place the slider in the first column
        with slider_col[0]:
            selection = st.select_slider("Choose", options=["Day", "Hour"])

        if selection == "Day":
            # Display the interactive chart
            col2.plotly_chart(fig_day, use_container_width=True)

        elif selection == "Hour":
            # Display the interactive chart
            col2.plotly_chart(fig_hour, use_container_width=True)

    st.title("Frequently Asked Questions (FAQs)")

    # Get the top 5 FAQ intents
    top_intents = get_top_FAQ_intents()

    if not top_intents:
        st.warning("No FAQ data available.")
    else:
        for index, (intent, data) in enumerate(top_intents.items(), start=1):
            # # Define different background colors for each block
            # if index % 2 == 0:
            #     background_color = "lightblue"
            # else:
            #     background_color = "lightgreen"

            # Apply the background color using HTML and CSS
            st.write(
                f'<div style="background-color: white; margin: 20px ; padding: 10px; border-radius: 5px; border: 2px solid black;">'
                f"<h4 style='color: black;'> {data['question']}</h4>"
                f"<h5 style='color: black;'><b>People asked:{data['count']}</b> </h5>"
                "</div>",
                unsafe_allow_html=True,
            )


if __name__ == "__main__":
    main()
