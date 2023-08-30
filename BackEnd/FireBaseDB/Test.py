import pyrebase
import json
from datetime import datetime
import hashlib  # For password hashing
import secrets  # For generating secure tokens

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

firebase = pyrebase.initialize_app(firebaseConfig)
pyrebase_db = firebase.database()

# Function to hash passwords before storage
def hash_password(password):
    salt = "random_salt_here"  # Add a random salt for security
    return hashlib.sha256((password + salt).encode()).hexdigest()

# Generate a unique account number by appending a number to the prefix
def generate_account_id(prefix, existing_account_numbers):

    account_number = prefix
    count = 1
    while account_number in existing_account_numbers:
        count += 1
        account_number = f"{prefix}{count}"

    return account_number

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

# Function to generate a secure token
def generate_token():
    return secrets.token_hex(32)  # Generate a 64-character (256-bit) token

# Login with Account ID and Password
def LoginWithCredentials(accountNumber, password):
    # Verify the entered credentials against the stored account data
    account_data = pyrebase_db.child("Account").child(accountNumber).get().val()
    if account_data:
        stored_password = account_data.get("password")
        hashed_password = hash_password(password)
        if stored_password == hashed_password:
            # Generate and store a secure token for this user
            token = generate_token()
            pyrebase_db.child("Account").child(accountNumber).child("token").set(token)
            return token
    return None
# Get Account Details Using Token ---------------------------------------------
def GetAccountWithToken(token):
    # Query the database to find the user account associated with the provided token
    users = pyrebase_db.child("Account").order_by_child("token").equal_to(token).get()
    if users:
        user_account = next(iter(users.val().items()))  # Get the first user found
        return user_account[0]  # Return the account number
    return None

# Get Account Details ---------------------------------------------
def GetAccount(accountNumber, password):
    if AuthenticateUser(accountNumber, password):
        print(pyrebase_db.child("Account").child(accountNumber).get().val())
    else:
        print("Authentication failed. Please check your account number and password.")

# ... other functions ...

# Example usage:
# CreateAccount("kavijajak", "kavi@gmail.com", "Savings", 5000, "password")
# GetAccount("ACC7", "password")
