import pyrebase
from datetime import datetime
import hashlib  # For password hashing
import json

from .access_db import auth, pyrebase_db

# Function to save chat data for a specific user
def save_chat_data(User_msg,Assistance_msg, intent,accountNumber):
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    chat_data = {
        "User_id":accountNumber,  # Use the UID as the user ID
        "User_msg": User_msg,
        "Assistance_msg":Assistance_msg,
        "Intent": intent,
        "timestamp": current_datetime
    }
    pyrebase_db.child("chat_history").child(accountNumber).push(chat_data)


# method that adds 1 to the "positive" count for a specific intent
def add_positive_count(intent):
    # First, retrieve the current positive count
    current_positive_count = pyrebase_db.child("intent").child(intent).child("positive").get()
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
    current_negative_count = pyrebase_db.child("intent").child(intent).child("negative").get()
    if current_negative_count is not None:
        current_negative_count = current_negative_count.val()
    else:
        current_negative_count = 0

    current_positive_count = pyrebase_db.child("intent").child(intent).child("positive").get()
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

def delete_chat_history(user_id):
    pyrebase_db.child("chat_history").child(user_id).remove()