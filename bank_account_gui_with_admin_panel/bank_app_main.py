# main.py

import json
import os
from bank_account import BankAccount  # Import the BankAccount class from a separate module

DATA_FILE = "accounts.json"  # JSON file used to store account data persistently

# Function to load all saved accounts from the JSON file
def load_accounts():
    if not os.path.exists(DATA_FILE):
        return {}  # Return an empty dictionary if the file doesn't exist
    
    with open(DATA_FILE, "r") as file:
        raw_data = json.load(file)  # Load JSON data from the file

    # Convert raw dictionary data into BankAccount objects
    return {
        name: BankAccount(
            data["balance"],
            data["acct_name"],
            data["password"],
            data["first_name"],
            data["middle_name"],
            data["last_name"]
        )
        for name, data in raw_data.items()
    }

# Function to save all account objects back into the JSON file
def save_accounts(accounts):
    with open(DATA_FILE, "w") as file:
        # Convert each BankAccount object into a dictionary for JSON saving
        json.dump({
            name: {
                "balance": acc.get_balance(),          # Use method to get balance
                "acct_name": acc._acct_name,
                "password": acc._password,
                "first_name": acc._first_name,
                "middle_name": acc._middle_name,
                "last_name": acc._last_name
            }
            for name, acc in accounts.items()
        }, file, indent=4)  # Save with indentation for readability
