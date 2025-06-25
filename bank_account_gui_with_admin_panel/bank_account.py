# Import necessary modules for GUI, file handling, and JSON operations

# Define the JSON file that stores all account data

class BankAccount: # Define the BankAccount class
    def __init__(self, balance, acct_name, password, first_name, middle_name, last_name): # Initialize a bank account with balance, username, password, and full name details
        # Define the BankAccount class to handle account operations:
        # saving data, formatting full name, verifying login, and managing transactions.
        self._balance = balance
        self._acct_name = acct_name
        self._password = password
        self._first_name = first_name
        self._middle_name = middle_name
        self._last_name = last_name

    # Return the full name of the user with middle initial if available
    # Example: "Juan C. Dela Cruz"
    def get_full_name(self):
        middle_initial = (self._middle_name[0] + ".") if self._middle_name else ""
        return f"{self._first_name} {middle_initial} {self._last_name}".strip()
    
    # Add the specified amount to the account balance if it is greater than zero
    def deposit(self, amount):
        if amount > 0:
            self._balance += amount

    # Subtract the specified amount from the balance if it's valid and sufficient
    # Raise an error if the amount is invalid or exceeds the current balance
    def withdraw(self, amount):
        if amount > 0 and self._balance >= amount:
            self._balance -= amount
        else:
            raise ValueError("Insufficient funds or invalid amount.")
