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

# Define the BankApp class that handles the entire GUI
    # Initialize the root window and set title, theme, and layout
    # Load accounts from the JSON file or initialize empty dict
    # Setup frames: main (signup), login, and transaction
    # Build the main account creation screen

    # Function to load account data from the JSON file
        # Read file and convert each entry to a BankAccount object

    # Function to save all current account data to the JSON file

    # Function to switch between different frames (main, login, transaction)

    # Function to build the main account creation interface
        # Clear previous widgets
        # Display labels and entry fields for all required data
        # Add "Create Account" and "Login" buttons

    # Function to build the login interface
        # Clear widgets
        # Add username and password entry
        # Add "Login" and "Back" buttons

    # Function to build the transaction interface after login
        # Show full name and balance
        # Add entry to input amount
        # Add "Deposit", "Withdraw", and "Logout" buttons

    # Function to create an account
        # Get values from entry fields
        # Check for password match and existing username
        # Convert inputs into BankAccount object
        # Save the account and switch to login screen

    # Function to login to an account
        # If admin credentials entered, show manager panel
        # Otherwise, verify credentials and show transaction screen

    # Function to show the admin panel
        # Open a new window listing all accounts
        # Show full name, username, and balance of each account
        # Allow deletion of account by entering username
        # Confirm deletion before proceeding

    # Function to log out of the current account
        # Reset current account
        # Save account data
        # Return to login screen

    # Function to handle deposits
        # Convert input to float
        # Call deposit method and update balance
        # Save and show success message

    # Function to handle withdrawals
        # Convert input to float
        # Call withdraw method
        # Catch errors like insufficient funds
        # Save and show result

    # Function to update balance label with the current value

# Start the application by creating the root window and running the main loop
