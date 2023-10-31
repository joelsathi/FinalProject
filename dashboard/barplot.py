import streamlit as st
import pyrebase
from datetime import datetime
import hashlib  # For password hashing
import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px

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
print(data)
# Create a list of dictionaries with the desired structure
intent_data_list = [
    {
        "Intent": intent,
        "Positive": intent_data["positive"],
        "Negative": intent_data["negative"],
    }
    for intent, intent_data in data.items()
]

# Create a DataFrame
df = pd.DataFrame(intent_data_list)

# Create a Streamlit app
st.title("Interactive Clustered Bar Chart of Intents")
st.write("Hover over the bars to see the count values:")

# Create an interactive clustered bar chart using Plotly
fig = px.bar(
    df,
    x="Intent",
    y=["Positive", "Negative"],
    title="Clustered Bar Chart of Intents",
    labels={"value": "Counts"},
    color_discrete_map={"Positive": "palegreen", "Negative": "lightcoral"},
)

# Add hover text to display count values
fig.update_traces(
    hovertemplate='<span style="font-size: 14px; color: white;"> %{x}: %{y} units</span>',
)

# Customize layout
fig.update_layout(
    xaxis_title="Intents",
    yaxis_title="Counts",
    barmode="group",
)

# Display the interactive chart
st.plotly_chart(fig)

# # Create a DataFrame
# df = pd.DataFrame(intent_data_list)
# chart_data = pd.DataFrame(intent_data_list, columns=["Postive", "Negative"])
# st.bar_chart(chart_data)
# # Create a Streamlit app
# st.title("Sentiment Analysis of Intents")
# st.write("Comparison of Positive and Negative Counts for Different Intents")

# # Use CSS color codes for custom colors
# colors = ["#00ff00", "#ff0000"]

# st.bar_chart(df, x="Intents", use_container_width=True, color=colors)
# plt.xticks(range(len(intents)), intents, rotation=45)
# plt.xlabel("Intents")
# plt.ylabel("Counts")
# st.pyplot()
