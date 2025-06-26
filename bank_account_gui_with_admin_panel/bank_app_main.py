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


    def build_main_frame(self):
        # Display the main (registration) frame and clear previous widgets
        self.show_frame(self.main_frame)
        for widget in self.main_frame.winfo_children():
            widget.destroy()  # Remove existing widgets to avoid duplication

        # Define the form fields for registration
        fields = ["First Name", "Middle Name", "Last Name", "Account Name", "Initial Deposit", "Password", "Confirm Password"]
        self.entries = {}  # Dictionary to store the entry widgets for each field

        # Create labels and entry fields for each form input
        for i, field in enumerate(fields):
            # Create label
            tk.Label(self.main_frame, text=field + ":", bg="white").grid(row=i, column=0, sticky="e", pady=2)
            
            # Create entry; hide input if it's a password field
            entry = tk.Entry(self.main_frame, show="*" if "Password" in field else None)
            entry.grid(row=i, column=1, pady=2)

            self.entries[field] = entry  # Store the entry widget for later access

        # Create button to trigger account creation
        tk.Button(
            self.main_frame,
            text="Create Account",
            command=self.create_account,
            bg="#800000", fg="white"
        ).grid(row=len(fields), columnspan=2, pady=10)

        # Create button to switch to login frame
        tk.Button(
            self.main_frame,
            text="Already have an account? Login",
            command=self.build_login_frame,
            bg="white"
        ).grid(row=len(fields)+1, columnspan=2)


    def create_account(self):
        try:
            # Collect and strip all input values from the registration form
            data = {k: self.entries[k].get().strip() for k in self.entries}
            
            # Try to convert initial deposit to a float
            amount = float(data["Initial Deposit"])

            # Check if passwords match
            if data["Password"] != data["Confirm Password"]:
                tk.messagebox.showerror("Error", "Passwords do not match.")
                return

            # Check if account name already exists
            if data["Account Name"] in self.accounts:
                tk.messagebox.showerror("Error", "Account name already exists.")
                return

            # Prepare data to pass into BankAccount constructor
            account_data = {
                "balance": amount,
                "acct_name": data["Account Name"],
                "password": data["Password"],
                "first_name": data["First Name"],
                "middle_name": data["Middle Name"],
                "last_name": data["Last Name"]
            }

            # Create new BankAccount instance and store it in the accounts dictionary
            new_account = BankAccount(**account_data)
            self.accounts[data["Account Name"]] = new_account

            # Save updated accounts to JSON file
            self.save_accounts()

            # Notify user and switch to login screen
            tk.messagebox.showinfo("Success", "Account created! Please log in.")
            self.build_login_frame()

        except ValueError:
            # Handle non-numeric or invalid deposit value
            tk.messagebox.showerror("Error", "Invalid amount entered.")

# Run the app
if __name__ == "__main__":
    root = tk.Tk()          # Create the main application window
    app = BankApp(root)     # Instantiate the banking app
    root.mainloop()         # Start the Tkinter main event loop
