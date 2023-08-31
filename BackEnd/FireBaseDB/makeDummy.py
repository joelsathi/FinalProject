import pyrebase
from datetime import datetime
import hashlib

firebaseConfig = {
  "apiKey": "AIzaSyDTrPMLJ9PnNqPPiY4KETnMAkNXSDVf1iM",
  'authDomain': "botmora-25373.firebaseapp.com",
  "databaseURL": "https://botmora-25373-default-rtdb.firebaseio.com",
  "projectId": "botmora-25373",
  "storageBucket": "botmora-25373.appspot.com",
  "messagingSenderId": "223313770308",
  "appId": "1:223313770308:web:bdb2bb2e428ddf11a70911",
  "measurementId": "G-ZPYWSE9S0J"
}

# Firebase Authentication

firebase=pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

# Firebase Database

db=firebase.database() # Database



# Function to hash passwords before storage
def hash_password(password):
    salt = "random_salt_here"  # Add a random salt for security
    return hashlib.sha256((password + salt).encode()).hexdigest()
# Create New Account ---------------------------------------------
def CreateAccount(UserName, userEmail, userAccountType, InitialBalance, password):

    hashed_password = hash_password(password)

    user=auth.create_user_with_email_and_password(userEmail,password)

    current_datetime = datetime.now()
    transactionRecipient = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

    account_data = {
        "name": UserName,
        "email": userEmail,
        "account_type": userAccountType,
        "balance": InitialBalance,
        "account_number": user['localId'],
        "password": hashed_password,  # Store the hashed password
        "transactions": {
            "type": "Open Account",
            "amount": InitialBalance,
            "recipient": transactionRecipient
        }
    }
    db.child("Account").child(user['localId']).set(account_data)

    print(f"Account {user['localId']} has been created with an initial balance of {InitialBalance} {userAccountType} for {UserName} at {transactionRecipient}")
    # return accountNumber



def GetBalance(accountNumber):
    return db.child("Account").child(accountNumber).child("balance").get().val()
# Update Balance of Account
def UpdateBalance(accountNumber, newBalance):
    db.child("Account").child(accountNumber).child("balance").set(newBalance)
def CreateTransaction(accountNumber, transactionType, transactionAmount):
    # Get the current date and time
    current_datetime = datetime.now()
    transactionRecipient= current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    
    transaction_data = {
        "type": transactionType,
        "amount": transactionAmount,
        "recipient": transactionRecipient
    }

    db.child("Account").child(accountNumber).child("transactions").push(transaction_data)
    if transactionType == "Deposit":
        newBalance = GetBalance(accountNumber) + transactionAmount
        UpdateBalance(accountNumber, newBalance)
    elif transactionType == "Withdraw":
        newBalance = GetBalance(accountNumber) - transactionAmount
        UpdateBalance(accountNumber, newBalance)
    else:
        print("Error: Invalid Transaction Type")

    print(f"Transaction of {transactionAmount} {transactionType} has been made to account {accountNumber} at {transactionRecipient}")



# CreateAccount("sada", "sada@gmail.com", "Savings", 5000, "123456")
# CreateTransaction("ACC6", "Deposit", 5000)
# CreateTransaction("ACC6", "Withdraw", 3500)



