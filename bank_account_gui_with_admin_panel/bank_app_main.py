import tkinter as tk
from bank_account import BankAccount  # Import the BankAccount class
import json
import os

DATA_FILE = "accounts.json"  # File to store account data persistently

class BankApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Grow a Garden: Banko Sheckles ng PUP (BSP)")  # Set window title
        self.root.configure(bg="#800000")  # Set maroon background to match PUP theme

        # Load account data from JSON file
        self.accounts = self.load_accounts()
        self.current_account = None  # Will hold the logged-in account object

        # Add a small slogan label above the title
        self.grow_label = tk.Label(
            self.root,
            text="Grow a Garden",
            font=("Arial", 8, "bold"),
            fg="white",
            bg="#800000"
        )
        self.grow_label.pack()

        # Add the main title/header label
        self.header = tk.Label(
            self.root,
            text="Banko Sheckles ng PUP (BSP)",
            font=("Arial", 16, "bold"),
            fg="white",
            bg="#800000"
        )
        self.header.pack()

        # Initialize the three main frames of the app
        self.main_frame = tk.Frame(self.root, bg="white")         # Registration frame
        self.login_frame = tk.Frame(self.root, bg="white")        # Login frame
        self.transaction_frame = tk.Frame(self.root, bg="white")  # Transaction frame

        # Start the app on the registration screen
        self.build_main_frame()


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


    def show_frame(self, frame):
        # Hide all frames first to ensure only one is visible at a time
        for f in (self.main_frame, self.login_frame, self.transaction_frame):
            f.pack_forget()

        # Display the selected frame with padding
        frame.pack(padx=20, pady=20)


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


    def build_login_frame(self):
        # Show the login frame and clear any existing widgets
        self.show_frame(self.login_frame)
        for widget in self.login_frame.winfo_children():
            widget.destroy()  # Remove previous widgets to prevent duplication

        # Label and entry for Account Name
        tk.Label(self.login_frame, text="Account Name:", bg="white").grid(row=0, column=0, pady=5)
        self.login_name = tk.Entry(self.login_frame)
        self.login_name.grid(row=0, column=1, pady=5)

        # Label and entry for Password
        tk.Label(self.login_frame, text="Password:", bg="white").grid(row=1, column=0, pady=5)
        self.login_password = tk.Entry(self.login_frame, show="*")  # Mask input for security
        self.login_password.grid(row=1, column=1, pady=5)

        # Login button that triggers login_account() method
        tk.Button(
            self.login_frame,
            text="Login",
            command=self.login_account,
            bg="#800000",
            fg="white"
        ).grid(row=2, columnspan=2, pady=10)

        # Button to go back to the registration screen
        tk.Button(
            self.login_frame,
            text="Back",
            command=self.build_main_frame,
            bg="white"
        ).grid(row=3, columnspan=2)


    def build_transaction_frame(self):
        # Display the transaction frame and remove previous widgets
        self.show_frame(self.transaction_frame)
        for widget in self.transaction_frame.winfo_children():
            widget.destroy()  # Clear frame to avoid duplicate UI elements

        # Greeting label showing the full name of the logged-in user
        tk.Label(
            self.transaction_frame,
            text=f"Welcome, {self.current_account.get_full_name()}",
            font=("Arial", 14),
            bg="white"
        ).grid(row=0, columnspan=2, pady=10)

        # Label that will display the user's current balance (updated dynamically)
        self.balance_label = tk.Label(
            self.transaction_frame,
            text="",  # initially empty; updated by self.update_balance()
            font=("Arial", 12, "bold"),
            bg="white"
        )
        self.balance_label.grid(row=1, columnspan=2)

        self.update_balance()  # Show current balance right after logging in

        # Label and entry for entering deposit or withdrawal amount
        tk.Label(self.transaction_frame, text="Amount:", bg="white").grid(row=2, column=0)
        self.transact_amount = tk.Entry(self.transaction_frame)
        self.transact_amount.grid(row=2, column=1)

        # Deposit button
        tk.Button(
            self.transaction_frame,
            text="Deposit",
            command=self.deposit,
            bg="#800000",
            fg="white"
        ).grid(row=3, column=0, pady=5)

        # Withdraw button
        tk.Button(
            self.transaction_frame,
            text="Withdraw",
            command=self.withdraw,
            bg="#800000",
            fg="white"
        ).grid(row=3, column=1, pady=5)

        # Logout button
        tk.Button(
            self.transaction_frame,
            text="Logout",
            command=self.logout,
            bg="white"
        ).grid(row=4, columnspan=2, pady=10)


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


    def login_account(self):
        # Get the username and password from the login form
        name = self.login_name.get().strip()
        password = self.login_password.get().strip()

        # Special login: if credentials match DATABASE2006, open manager panel
        if name == "DATABASE2006" and password == "2006":
            self.show_manager_panel()
            return

        # Check if the entered account exists
        account = self.accounts.get(name)

        # Validate credentials using the BankAccount's verify_credentials method
        if account and account.verify_credentials(name, password):
            self.current_account = account  # Set current logged-in account
            self.build_transaction_frame()  # Go to transaction interface
        else:
            # Show error if login fails
            tk.messagebox.showerror("Login Failed", "Invalid credentials.")


    def show_manager_panel(self):
        # Create a new window for the database manager
        manager_window = tk.Toplevel(self.root)
        manager_window.title("Database Manager Panel")
        manager_window.configure(bg="white")

        # Title label
        tk.Label(manager_window, text="All Accounts", font=("Arial", 12, "bold"), bg="white").pack(pady=5)

        # Display information about all accounts
        accounts_info = ""
        for user, acc in self.accounts.items():
            accounts_info += f"{acc.get_full_name()} | Username: {user} | Balance: ₪{acc.get_balance():.2f}\n"

        # If no accounts exist, show a placeholder message
        info_label = tk.Label(
            manager_window,
            text=accounts_info or "No accounts found.",
            bg="white",
            justify="left"
        )
        info_label.pack(padx=10, pady=5)

        # Input field to enter username of the account to delete
        tk.Label(manager_window, text="Username to Delete:", bg="white").pack()
        self.delete_entry = tk.Entry(manager_window)
        self.delete_entry.pack(pady=5)

        # Define the delete_account function to handle deletion logic
        def delete_account():
            username = self.delete_entry.get().strip()
            if username in self.accounts:
                # Confirm with the manager before deleting the account
                confirm = tk.messagebox.askyesno(
                    "Confirm Deletion",
                    f"Are you sure you want to delete account '{username}'?"
                )
                if confirm:
                    del self.accounts[username]         # Delete the account
                    self.save_accounts()                # Save changes
                    tk.messagebox.showinfo("Deleted", f"Account '{username}' has been deleted.")
                    manager_window.destroy()            # Close the window to refresh it
            else:
                # Show error if username does not exist
                tk.messagebox.showerror("Error", f"No account found with username '{username}'.")

        # Button to trigger the delete_account function
        tk.Button(
            manager_window,
            text="Delete Account",
            command=delete_account,
            bg="red",
            fg="white"
        ).pack(pady=10)


    def logout(self):
        # Clear the current logged-in account
        self.current_account = None

        # Save any changes made during the session (optional but safe)
        self.save_accounts()

        # Redirect the user back to the login screen
        self.build_login_frame()


    def deposit(self):
        try:
            # Get the amount entered by the user and convert it to float
            amount = float(self.transact_amount.get())

            # Perform the deposit on the current account
            self.current_account.deposit(amount)

            # Save updated account data to the JSON file
            self.save_accounts()

            # Show confirmation message
            tk.messagebox.showinfo("Success", f"₪{amount:.2f} deposited.")

            # Update the balance display on the transaction screen
            self.update_balance()

        except ValueError:
            # Handle invalid input (e.g., letters or empty string)
            tk.messagebox.showerror("Error", "Invalid amount.")


    def withdraw(self):
        try:
            # Get the amount entered by the user and convert it to float
            amount = float(self.transact_amount.get())

            # Attempt to withdraw the amount from the current account
            self.current_account.withdraw(amount)

            # Save updated account data to the JSON file
            self.save_accounts()

            # Show confirmation message
            tk.messagebox.showinfo("Success", f"₪{amount:.2f} withdrawn.")

            # Update the balance display on the transaction screen
            self.update_balance()

        except ValueError as e:
            # Handle invalid input or errors from the withdraw() method (e.g., insufficient funds)
            tk.messagebox.showerror("Error", str(e))


    def update_balance(self):
        # Get the current balance from the logged-in account
        balance = self.current_account.get_balance()

        # Update the label in the transaction frame to show the latest balance
        self.balance_label.config(text=f"Balance: ₪{balance:.2f}")


# Run the app
if __name__ == "__main__":
    root = tk.Tk()          # Create the main application window
    app = BankApp(root)     # Instantiate the banking app
    root.mainloop()         # Start the Tkinter main event loop
