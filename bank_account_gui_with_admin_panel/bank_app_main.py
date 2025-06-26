import tkinter as tk
from bank_account import BankAccount  # Import the BankAccount class
import json
import os

DATA_FILE = "accounts.json"  # File to store account data persistently

class BankApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Grow a Garden: Banko Sheckles ng PUP (BSP)")  # App window title
        self.root.configure(bg="#800000")  # Set background color to maroon (PUP theme)

        self.accounts = self.load_accounts()  # Load existing accounts from JSON file
        self.current_account = None  # Will hold the currently logged-in account

        # Define main GUI frames
        self.main_frame = tk.Frame(self.root, bg="white")        # Registration frame
        self.login_frame = tk.Frame(self.root, bg="white")       # Login frame
        self.transaction_frame = tk.Frame(self.root, bg="white") # Transaction frame

        self.show_frame(self.main_frame)  # Show registration frame by default

    def show_frame(self, frame):
        """Switch to the given frame and hide others."""
        for f in (self.main_frame, self.login_frame, self.transaction_frame):
            f.pack_forget()  # Hide all frames
        frame.pack(padx=20, pady=20)  # Show the selected frame

    def load_accounts(self):
        """Load account data from the JSON file and return a dictionary of BankAccount objects."""
        if not os.path.exists(DATA_FILE):
            return {}  # Return empty dict if file doesn't exist

        with open(DATA_FILE, "r") as file:
            raw_data = json.load(file)

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

    def save_accounts(self):
        """Save all BankAccount objects into the JSON file for persistence."""
        with open(DATA_FILE, "w") as file:
            json.dump({
                name: {
                    "balance": acc.get_balance(),       # Use method to get balance
                    "acct_name": acc._acct_name,
                    "password": acc._password,
                    "first_name": acc._first_name,
                    "middle_name": acc._middle_name,
                    "last_name": acc._last_name
                }
                for name, acc in self.accounts.items()
            }, file, indent=4)  # Save with indentation for readability


# Run the app
if __name__ == "__main__":
    root = tk.Tk()          # Create the main application window
    app = BankApp(root)     # Instantiate the banking app
    root.mainloop()         # Start the Tkinter main event loop
