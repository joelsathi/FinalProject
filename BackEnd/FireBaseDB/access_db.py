import pyrebase
from datetime import datetime
import hashlib  # For password hashing
import json

firebaseConfig = {
  "apiKey": "AIzaSyDTrPMLJ9PnNqPPiY4KETnMAkNXSDVf1iM",
  "authDomain": "botmora-25373.firebaseapp.com",
  "databaseURL": "https://botmora-25373-default-rtdb.firebaseio.com",
  "projectId": "botmora-25373",
  "storageBucket": "botmora-25373.appspot.com",
  "messagingSenderId": "223313770308",
  "appId": "1:223313770308:web:bdb2bb2e428ddf11a70911",
  "measurementId": "G-ZPYWSE9S0J"
}

firebase=pyrebase.initialize_app(firebaseConfig)
pyrebase_db=firebase.database()

auth = firebase.auth()

# Get Balance of Account
def GetBalance(accountNumber):
    return pyrebase_db.child("Account").child(accountNumber).child("balance").get().val()

# Get Account Details ---------------------------------------------
def GetAccountDetails(accountNumber):
    balance = pyrebase_db.child("Account").child(accountNumber).child("balance").get().val()
    name = pyrebase_db.child("Account").child(accountNumber).child("name").get().val()
    account_type = pyrebase_db.child("Account").child(accountNumber).child("account_type").get().val()
    email = pyrebase_db.child("Account").child(accountNumber).child("email").get().val()

    return f"Name: {name} Account Type: {account_type} Email: {email} Balance: {balance}"

# Get account number of user ---------------------------------------------
def GetAccountNumber(accountNumber):
    return pyrebase_db.child("Account").child(accountNumber).child("account_number").get().val()

# Get Account Name ---------------------------------------------
def GetAccountName(accountNumber):
    return pyrebase_db.child("Account").child(accountNumber).child("name").get().val()

# Get Account Type ---------------------------------------------
def GetAccountType(accountNumber):
    return pyrebase_db.child("Account").child(accountNumber).child("account_type").get().val()

# Get Account Email ---------------------------------------------
def GetAccountEmail(accountNumber):
    return pyrebase_db.child("Account").child(accountNumber).child("email").get().val()

# Get All Transactions of Account ---------------------------------------------
def GetTransactions(accountNumber):
    try:
      transactions=pyrebase_db.child("Account").child(accountNumber).child("transactions").get()
    except:
      transactions = None
    try:
      tr=""
      for transaction in transactions:tr= tr + f" {transaction.val()['type']} {transaction.val()['amount']} {transaction.val()['recipient']}"
      return tr
    except:
      print("No transactions found")


# Function to get the latest chat messages for a specific user and return as a JSON object
def get_latest_chat_history(user_id, limit=5):
    try:
        chat_history = pyrebase_db.child("chat_history").child(user_id).order_by_child("timestamp").limit_to_last(limit).get()
        chat_data = chat_history.val()
        if chat_data:
            chat_list = [chat_data[key] for key in chat_data]
            chat_list.reverse()  # Reverse the list to get the latest messages first
            # Build a JSON object
            chat_json = json.dumps({"chat_history": chat_list})
            return chat_json
        else:
            return json.dumps({"chat_history": []})
    except Exception as e:
        print(f"Error: {e}")
        return json.dumps({"error": str(e)})
    
# last transactions as a JSON object
def read_last_transactions(accountNumber, limit=5):
    try:
        # Retrieve all transactions for the account
        transactions = pyrebase_db.child("Account").child(accountNumber).child("transactions").get()

        if transactions is not None:
            transaction_data = transactions.val()
            if transaction_data:
                # Convert the transaction data to a list of dictionaries
                transaction_list = list(transaction_data.values())
                # Sort the transactions by timestamp in descending order (latest first)
                sorted_transactions = sorted(transaction_list, key=lambda x: x['timestamp'], reverse=True)
                # Get the last transactions up to the specified limit
                last_transactions = sorted_transactions[:limit]
                return json.dumps({"transactions": last_transactions})
        else:
            return json.dumps({"transactions": []})

    except Exception as e:
        print(f"Error: {e}")
        return json.dumps({"error": str(e)})


# Function to get the top 5 intents and their data as a JSON object in FAQ
def get_top_FAQ_intents(limit=5):
    try:
        # Retrieve all FAQ intents and their data
        faq_intents = pyrebase_db.child("FAQ").get()

        if faq_intents is not None:
            faq_data = faq_intents.val()
            if faq_data:
                # Sort the FAQ intents by count in descending order
                sorted_faq_intents = sorted(faq_data.items(), key=lambda x: x[1]["count"], reverse=True)
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



