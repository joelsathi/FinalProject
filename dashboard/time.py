import streamlit as st
import json
import pyrebase
import plotly.express as px
import pandas as pd

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

time_data = pyrebase_db.child("Time_stamp").get().val()

# Assuming time_data is a list of dictionaries with days and other keys
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

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


df = pd.DataFrame(day_data_list)
# Create an interactive clustered bar chart using Plotly
fig = px.bar(
    df,
    x="Day",
    y=["Count"],
    labels={"value": "Counts"},
    # color_discrete_map={"Positive": "palegreen", "Negative": "lightcoral"},
)

st.plotly_chart(fig)
