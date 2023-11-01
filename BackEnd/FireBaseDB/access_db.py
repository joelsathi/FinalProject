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


def convert_to_desired_format(chat_history):
    formatted_chats = []
    for chat_data in chat_history:
        user_msg = {
            "role": "user",
            "content": chat_data["User_msg"]
        }
        assistant_msg = {
            "role": "assistant",
            "content": chat_data["Assistance_msg"]
        }
        formatted_chats.append(user_msg)
        formatted_chats.append(assistant_msg)
    # convert the list of dictionaries to a JSON object

    cur = {"chats": formatted_chats}

    json_object = json.dumps(cur, indent=2)

    return json_object

def get_latest_chat_history(user_id, limit=5):
    try:
        chat_history = pyrebase_db.child("chat_history").child(user_id).order_by_child("timestamp").limit_to_last(limit).get()
        chat_data = chat_history.val()
        if chat_data:
            chat_list = [chat_data[key] for key in chat_data]
            chat_list.reverse()  # Reverse the list to get the latest messages first
            formatted_data = convert_to_desired_format(chat_list)
            return formatted_data
        else:
            return json.dumps({"chats": []}, indent=2)
    except Exception as e:
        print(f"Error: {e}")
        return {"error": str(e)}
   
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
                
                formatted_transactions = ""
                for transaction in last_transactions:
                    title = transaction.get("Title", "")
                    amount = transaction.get("amount", "")
                    timestamp = transaction.get("timestamp", "")
                    transaction_type = transaction.get("type", "")

                    formatted_transactions += f"Title: {title}, Amount: {amount}, Timestamp: {timestamp}, Type: {transaction_type}\n"

                return formatted_transactions
        else:
            return "No transactions found."

    except Exception as e:
        print(f"Error: {e}")
        return str(e)


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

from tabulate import tabulate

# install - pip install firebase-admin tabulate

def Get_Saving_Interest_Rates():
    # Reference to the "Savings_rates" node in your database
    savings_rates_ref = pyrebase_db.child("Savings_rates")

    # Retrieve the data as a dictionary
    savings_data = savings_rates_ref.get().val()

    # Format the data as a list of lists for tabulation
    table_data = []

    if savings_data:
        for key, value in savings_data.items():
            table_data.append([value.get("Savings_account_type", ""), value.get("Annual_interest_rate", "")])

    # Create and print the table without the "Key" column
    if table_data:
        headers = ["Savings Account Type", "Annual Interest Rate"]
        table = tabulate(table_data, headers, tablefmt="pretty")
        return table
    else:
        print("No data found in the database.")


def Get_Fixed_Interset_Rates():
        # Reference to the "Savings_rates" node in your database
    savings_rates_ref = pyrebase_db.child("Fixed_rates")

    # Retrieve the data as a dictionary
    savings_data = savings_rates_ref.get().val()

    # Format the data as a list of lists for tabulation
    table_data = []

    if savings_data:
        for key, value in savings_data.items():
            table_data.append([value.get("Term & Payment method", ""), value.get("Interest rate", "")])

    # Create and print the table without the "Key" column
    if table_data:
        headers = ["Term & Payment method", "Fix Interest Rate"]
        table = tabulate(table_data, headers, tablefmt="pretty")
        return table
    else:
        print("No data found in the database.")

def Get_Loan_Rates():
        # Reference to the "Savings_rates" node in your database
    savings_rates_ref = pyrebase_db.child("Loan_rates")

    # Retrieve the data as a dictionary
    savings_data = savings_rates_ref.get().val()

    # Format the data as a list of lists for tabulation
    table_data = []

    if savings_data:
        for key, value in savings_data.items():
            table_data.append([key,value.get("interest_rate_per_month", ""), value.get("maximum_amount", ""),value.get("repayment_period","")])

    # Create and print the table without the "Key" column
    if table_data:
        headers = ["Type Of Loan","Interest Rate Per Month", "Fix Interest Rate","Repayment Period"]
        table = tabulate(table_data, headers, tablefmt="pretty")
        return table
    else:
        print("No data found in the database.")


def Get_Exchange_Rates():
    # Reference to the "Exchange_rates" node in your database
    exchange_rates_ref = pyrebase_db.child("Exchange_rates")

    # Retrieve the data as a dictionary
    exchange_data = exchange_rates_ref.get().val()
    print(exchange_data)

    # Format the data as a list of lists for tabulation
    table_data = []

    if exchange_data:
        for key, value in exchange_data.items():
            table_data.append([
                key,
                value.get("buying_rate_per_currency_in_LKR ", ""),
                value.get("currency_type", ""),
                value.get("selling_rate_per_currency_in_LKR", "")
            ])

        headers = ["Country", "Buying Rate Per Currency In LKR", "Currency Type", "Selling Rate per Currency In LKR"]
        table = tabulate(table_data, headers, tablefmt="pretty")
        return table
    else:
        return "No data found in the database."

