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

auth = firebase.auth()


# Get Balance of Account
def GetBalance(accountNumber):
    return pyrebase_db.child("Account").child(accountNumber).child("balance").get().val()


# Get Account Details ---------------------------------------------
def GetAccountDetails(accountNumber):
   return pyrebase_db.child("Account").child(accountNumber).get().val()

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



