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

def create_savings_rates(savings_acc_type, interest_rate):
    savings_rate_data = {
        "Savings_account_type": savings_acc_type,
        "Annual_interest_rate": interest_rate
    }

    db.child("Savings_rates").push(savings_rate_data)

# create_savings_rates("Ordinary Savings", "2.50%")
# create_savings_rates("Samurdhi Investment", "2.75%")
# create_savings_rates("18 + Youth Savings Account Scheme", "3.00%")
# create_savings_rates("14 + Teenagers' Savings Account Scheme", "3.50%")
# create_savings_rates("Senior Citizens Savings", "3.50%")


def create_fixed_rates(term_and_payement_method, interest_rate):
    fixed_rate_data = {
        "Term & Payment method": term_and_payement_method,
        "Interest rate": interest_rate
    }

    db.child("Fixed_rates").push(fixed_rate_data)

# create_fixed_rates("1 Month (LKR)", "9.00%")
# create_fixed_rates("3 Month (LKR)", "10.00%")
# create_fixed_rates("6 Month (LKR)", "9.50%")
# create_fixed_rates("1 Year -Interest at maturity (LKR)", "8.50%")
# create_fixed_rates("1 Year -Interest paid monthly (LKR)", "8.00%")
# create_fixed_rates("1 Year | Senior Citizens* -Interest at maturity (LKR)", "9.50%")
# create_fixed_rates("1 Year | Senior Citizens* -Interest paid monthly (LKR)", "9.25%")
# create_fixed_rates("2 Years -Interest at maturity (LKR)", "9.50%")
# create_fixed_rates("2 Years -Interest paid monthly (LKR)", "8.75%")
# create_fixed_rates("2 Years -Interest paid annually (LKR)", "9.00%")
# create_fixed_rates("5 Years -Interest at maturity (LKR)", "11.00%")
# create_fixed_rates("5 Years -Interest paid monthly (LKR)", "8.75%")
# create_fixed_rates("5 Years -Interest paid annually (LKR)", "9.00%")


# acc="zwGbr6s1CNY9JGZcmZRF1LOBza22"
# # Example data for 10 chat entries
# chat_data = [
#     {"User_msg": "Hello", "Assistance_msg": "Hi, how can I assist you?", "Intent": "Greeting"},
#     {"User_msg": "I'd like to check my balance.", "Assistance_msg": "Sure, please provide your account number.", "Intent": "Check Balance"},
#     {"User_msg": "My account number is 789012.", "Assistance_msg": "Thank you. Let me find your account.", "Intent": "Provide Account Number"},
#     {"User_msg": "What's my current balance?", "Assistance_msg": "Your current balance is $2,500.", "Intent": "Check Balance", "accountNumber": "789012"},
#     {"User_msg": "Can I transfer money to another account?", "Assistance_msg": "Yes, you can. Please provide the recipient's account number.", "Intent": "Transfer Money", "accountNumber": "789012"},
#     {"User_msg": "The recipient's account number is 345678.", "Assistance_msg": "Thank you. How much would you like to transfer?", "Intent": "Provide Recipient Account Number", "accountNumber": "789012"},
#     {"User_msg": "I want to transfer $500.", "Assistance_msg": "Your transfer of $500 has been initiated.", "Intent": "Transfer Money", "accountNumber": "789012"},
#     {"User_msg": "What's the interest rate for a savings account?", "Assistance_msg": "The current interest rate for our savings account is 2.5%.", "Intent": "Check Interest Rate", "accountNumber": "789012"},
#     {"User_msg": "Thank you for your help.", "Assistance_msg": "You're welcome! If you have any more questions, feel free to ask.", "Intent": "Greeting", "accountNumber": "789012"},
#     {"User_msg": "Goodbye", "Assistance_msg": "Goodbye! Have a great day!", "Intent": "Goodbye", "accountNumber": "789012"}
# ]

# # Loop through the chat data and add each entry to the database
# for entry in chat_data:
#     save_chat_data(entry["User_msg"], entry["Assistance_msg"], entry["Intent"], acc)
