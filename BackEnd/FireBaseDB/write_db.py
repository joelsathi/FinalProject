import pyrebase
from datetime import datetime
import hashlib  # For password hashing
import json
import numpy
import sklearn
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

# Load the Sentence Transformers model
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# from access_db import auth, pyrebase_db
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


# Function to save chat data for a specific user
def save_chat_data(User_msg, Assistance_msg, intent, accountNumber):
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    chat_data = {
        "User_id": accountNumber,  # Use the UID as the user ID
        "User_msg": User_msg,
        "Assistance_msg": Assistance_msg,
        "Intent": intent,
        "timestamp": current_datetime,
    }
    pyrebase_db.child("chat_history").child(accountNumber).push(chat_data)


# method that adds 1 to the "positive" count for a specific intent
def add_positive_count(intent):
    # First, retrieve the current positive count
    current_positive_count = (
        pyrebase_db.child("intent").child(intent).child("positive").get()
    )
    if current_positive_count is not None:
        current_positive_count = current_positive_count.val()
    else:
        current_positive_count = 0

    # Increment the positive count by 1
    new_positive_count = current_positive_count + 1

    # Set the updated positive count back in the database
    pyrebase_db.child("intent").child(intent).child("positive").set(new_positive_count)


# method that adds +1 to the "negative" count and subtracts -1 from the "positive" count for a specific intent
def add_negative_and_subtract_positive(intent):
    # Retrieve the current negative and positive counts
    current_negative_count = (
        pyrebase_db.child("intent").child(intent).child("negative").get()
    )
    if current_negative_count is not None:
        current_negative_count = current_negative_count.val()
    else:
        current_negative_count = 0

    current_positive_count = (
        pyrebase_db.child("intent").child(intent).child("positive").get()
    )
    if current_positive_count is not None:
        current_positive_count = current_positive_count.val()
    else:
        current_positive_count = 0

    # Increment the negative count by 1
    new_negative_count = current_negative_count + 1

    # Subtract 1 from the positive count
    if current_positive_count > 0:
        new_positive_count = current_positive_count - 1
    else:
        new_positive_count = 0

    # Set the updated negative and positive counts back in the database
    pyrebase_db.child("intent").child(intent).child("negative").set(new_negative_count)
    pyrebase_db.child("intent").child(intent).child("positive").set(new_positive_count)


# method that adds 1 to the count for a specific intent in FAQ
def add_FAQ_count(intent):
    # First, retrieve the current positive count
    current_count = pyrebase_db.child("FAQ").child(intent).child("count").get()
    if current_count is not None:
        current_count = current_count.val()
    else:
        current_count = 0

    # Increment the positive count by 1
    new_count = current_count + 1

    # Set the updated positive count back in the database
    pyrebase_db.child("FAQ").child(intent).child("count").set(new_count)


def add_FAQ_count(question):
    # First, retrieve the current positive count
    current_count_dict = pyrebase_db.child("FAQ").get().val()
    max_value = -1

    for key, value in current_count_dict.items():
        question_text = value["question"]
        embeddings = model.encode([question, question_text])
        similarity_value = cosine_similarity(embeddings)[0, 1]
        if similarity_value > max_value:
            key_value = key
            max_value = similarity_value
            select = question_text

    if max_value > 0.4:
        cur_count = current_count_dict[key_value]["count"] + 1
        pyrebase_db.child("FAQ").child(key_value).child("count").set(cur_count)

    else:
        select = question
        cur_count = 1
        question_data = {
            "question": select,
            "count": cur_count,
        }

        pyrebase_db.child("FAQ").push(question_data)

    time = pyrebase_db.child("Time_stamp").get().val()

    day = time[datetime.now().strftime("%A")]
    count_data = {"count": day["count"] + 1}
    pyrebase_db.child("Time_stamp").child(datetime.now().strftime("%A")).set(count_data)

    hour = time[datetime.now().strftime("%H")]
    count_data = {"count": hour["count"] + 1}
    pyrebase_db.child("Time_stamp").child(datetime.now().strftime("%H")).set(count_data)


# add_FAQ_count("What is the contact numeber?")
