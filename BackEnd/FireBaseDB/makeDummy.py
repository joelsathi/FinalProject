import pyrebase
from datetime import datetime
import hashlib

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

# Firebase Authentication

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

# Firebase Database

db = firebase.database()  # Database


# Function to hash passwords before storage
def hash_password(password):
    salt = "random_salt_here"  # Add a random salt for security
    return hashlib.sha256((password + salt).encode()).hexdigest()


# Create New Account ---------------------------------------------
def CreateAccount(UserName, userEmail, userAccountType, InitialBalance, password):
    hashed_password = hash_password(password)

    user = auth.create_user_with_email_and_password(userEmail, password)

    current_datetime = datetime.now()
    transactionRecipient = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

    account_data = {
        "name": UserName,
        "email": userEmail,
        "account_type": userAccountType,
        "balance": InitialBalance,
        "account_number": user["localId"],
        "password": hashed_password,  # Store the hashed password
        "transactions": {
            "type": "Open Account",
            "amount": InitialBalance,
            "recipient": transactionRecipient,
        },
    }
    db.child("Account").child(user["localId"]).set(account_data)

    print(
        f"Account {user['localId']} has been created with an initial balance of {InitialBalance} {userAccountType} for {UserName} at {transactionRecipient}"
    )
    # return accountNumber


def GetBalance(accountNumber):
    return db.child("Account").child(accountNumber).child("balance").get().val()


# Update Balance of Account
def UpdateBalance(accountNumber, newBalance):
    db.child("Account").child(accountNumber).child("balance").set(newBalance)


def CreateTransaction(accountNumber, transactionType, transactionAmount):
    # Get the current date and time
    current_datetime = datetime.now()
    transactionRecipient = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

    transaction_data = {
        "type": transactionType,
        "amount": transactionAmount,
        "recipient": transactionRecipient,
    }

    db.child("Account").child(accountNumber).child("transactions").push(
        transaction_data
    )
    if transactionType == "Deposit":
        newBalance = GetBalance(accountNumber) + transactionAmount
        UpdateBalance(accountNumber, newBalance)
    elif transactionType == "Withdraw":
        newBalance = GetBalance(accountNumber) - transactionAmount
        UpdateBalance(accountNumber, newBalance)
    else:
        print("Error: Invalid Transaction Type")

    print(
        f"Transaction of {transactionAmount} {transactionType} has been made to account {accountNumber} at {transactionRecipient}"
    )


# CreateAccount("sada", "sada@gmail.com", "Savings", 5000, "123456")
# CreateTransaction("ACC6", "Deposit", 5000)
# CreateTransaction("ACC6", "Withdraw", 3500)


# Create Exchange Rates ---------------------------------------------
def CreateExchangeRates(country, buying_rate, selling_rate, currency_type):
    # current_datetime = datetime.now()
    # transactionRecipient = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

    exchange_data = {
        "currency_type": currency_type,
        "buying_rate_per_currency_in_LKR ": buying_rate,
        "selling_rate_per_currency_in_LKR": selling_rate,
    }
    db.child("Exchange_rates").child(country).set(exchange_data)
    # return accountNumber


# CreateExchangeRates("USA", 323.25, 331.5, "USD")
# CreateExchangeRates("Europe", 336.12, 351.02, "EUR")
# CreateExchangeRates("England", 387.52, 402.69, "GBP")
# CreateExchangeRates("Australia", 201.36, 212.93, "AUD")
# CreateExchangeRates("Singapore", 230.23, 243.84, "SGD")


# Create Loan Rates ---------------------------------------------
def CreateLoanRates(name, interest_rate, maximum_amount, repayment_period):
    # current_datetime = datetime.now()
    # transactionRecipient = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

    loan_data = {
        "interest_rate_per_month": interest_rate,
        "maximum_amount": maximum_amount,
        "repayment_period": repayment_period,
    }
    db.child("Loan_rates").child(name).set(loan_data)
    # return accountNumber


# CreateLoanRates("Home Loan", 7.5, 10000000, 20)
# CreateLoanRates("Personal Loan", 8.5, 500000, 5)
# CreateLoanRates("Vehicle Loan", 9.5, 1000000, 10)
# CreateLoanRates("Education Loan", 6.5, 1000000, 10)


# Create DateStamp
def CreateTime():
    current_datetime = datetime.now()
    # transactionRecipient = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

    time_data = {
        "count": 1,
    }
    db.child("Time_stamp").child(current_datetime.strftime("%H")).set(time_data)
    db.child("Time_stamp").child(current_datetime.strftime("%A")).set(time_data)
    # return accountNumber


# weekdays = [
#     "Monday",
#     "Tuesday",
#     "Wednesday",
#     "Thursday",
#     "Friday",
#     "Saturday",
#     "Sunday",
# ]
# numbers = list(range(1, 25))
# for i in weekdays:
#     db.child("Time_stamp").child(i).set({"count": 0})
# for i in numbers:
#     db.child("Time_stamp").child(str(i)).set({"count": 0})


def createIntent(intent):
    intent_data = {
        "positive": 0,
        "negative": 0,
    }

    db.child("intent").child(intent).set(intent_data)


# createIntent("Transaction")
# createIntent("Exchange_rate")
# createIntent("Loan_rate")
# createIntent("Fixed_rate")
# createIntent("Savings_rate")
