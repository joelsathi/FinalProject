import pyrebase
from datetime import datetime
import hashlib  # For password hashing

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

# Generate a unique account number by appending a number to the prefix
def generate_account_id(prefix, existing_account_numbers):

    account_number = prefix
    count = 1
    while account_number in existing_account_numbers:
        count += 1
        account_number = f"{prefix}{count}"

    return account_number

# Function to hash passwords before storage
def hash_password(password):
    salt = "random_salt_here"  # Add a random salt for security
    return hashlib.sha256((password + salt).encode()).hexdigest()

# Create New Account ---------------------------------------------
def CreateAccount(UserName, userEmail, userAccountType, InitialBalance, password):
    # Generate a unique account ID
    existing_account_numbers = pyrebase_db.child('Account').shallow().get().val()
    account_prefix = "ACC"
    accountNumber = generate_account_id(account_prefix, existing_account_numbers)

    # Hash the provided password before storage
    hashed_password = hash_password(password)

    current_datetime = datetime.now()
    transactionRecipient = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    account_data = {
        "name": UserName,
        "email": userEmail,
        "account_type": userAccountType,
        "balance": InitialBalance,
        "account_number": accountNumber,
        "password": hashed_password,  # Store the hashed password
        "transactions": {
            "type": "Open Account",
            "amount": InitialBalance,
            "recipient": transactionRecipient
        }
    }
    pyrebase_db.child("Account").child(accountNumber).set(account_data)

    print(f"Account {accountNumber} has been created with an initial balance of {InitialBalance} {userAccountType} for {UserName} at {transactionRecipient}")
    # return accountNumber

# Authenticate user using account number and password
def AuthenticateUser(accountNumber, password):
    account_data = pyrebase_db.child("Account").child(accountNumber).get().val()
    if account_data:
        stored_password = account_data.get("password")
        hashed_password = hash_password(password)
        if stored_password == hashed_password:
            return True
    return False

# Create Transaction ---------------------------------------------

# Get Balance of Account
def GetBalance(accountNumber):
    return pyrebase_db.child("Account").child(accountNumber).child("balance").get().val()

# Update Balance of Account
def UpdateBalance(accountNumber, newBalance):
    pyrebase_db.child("Account").child(accountNumber).child("balance").set(newBalance)


def CreateTransaction(accountNumber, transactionType, transactionAmount):
    # Get the current date and time
    current_datetime = datetime.now()
    transactionRecipient= current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    
    transaction_data = {
        "type": transactionType,
        "amount": transactionAmount,
        "recipient": transactionRecipient
    }

    pyrebase_db.child("Account").child(accountNumber).child("transactions").push(transaction_data)
    if transactionType == "Deposit":
        newBalance = GetBalance(accountNumber) + transactionAmount
        UpdateBalance(accountNumber, newBalance)
    elif transactionType == "Withdraw":
        newBalance = GetBalance(accountNumber) - transactionAmount
        UpdateBalance(accountNumber, newBalance)
    else:
        print("Error: Invalid Transaction Type")

    print(f"Transaction of {transactionAmount} {transactionType} has been made to account {accountNumber} at {transactionRecipient}")
    # return transaction_data


# Get Account Details ---------------------------------------------
def GetAccount(accountNumber, password):
    if AuthenticateUser(accountNumber, password):
        print(pyrebase_db.child("Account").child(accountNumber).get().val())
        return pyrebase_db.child("Account").child(accountNumber).get().val()
    else:
        print("Authentication failed. Please check your account number and password.")

# Get All Transactions of Account ---------------------------------------------
def GetTransactions(accountNumber):
    try:
      transactions=pyrebase_db.child("Account").child(accountNumber).child("transactions").get()
    except:
      print("No transactions found")
    try:
      for transaction in transactions:
          # print(transaction.key())
          print(f" {transaction.val().get('recipient')} {transaction.val().get('type')} {transaction.val().get('amount')} ")
          print("")
    except:
      print("No transactions found")
    # return pyrebase_db.child("Account").child(accountNumber).child("transactions").get().val()



# CreateAccount("kavijajak", "kavi@gmail.com", "Savings", 5000)

# CreateTransaction("ACC6", "Deposit", 5000)
# CreateTransaction("ACC6", "Withdraw", 3500)

# GetTransactions("ACC6")

# GetAccount("ACC6")



