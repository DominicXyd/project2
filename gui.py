import tkinter as tk
from tkinter import messagebox
from logic import Account

class Application:
    def __init__(self, root):
        self.root = root
        self.root.title("Bank Account System")

        # Create UI elements for login or account creation
        self.first_name_label = tk.Label(root, text="First Name:")
        self.first_name_label.grid(row=0, column=0)
        self.first_name_entry = tk.Entry(root)
        self.first_name_entry.grid(row=0, column=1)

        self.last_name_label = tk.Label(root, text="Last Name:")
        self.last_name_label.grid(row=1, column=0)
        self.last_name_entry = tk.Entry(root)
        self.last_name_entry.grid(row=1, column=1)

        self.pin_label = tk.Label(root, text="Enter PIN:")
        self.pin_label.grid(row=2, column=0)
        self.pin_entry = tk.Entry(root, show="*")
        self.pin_entry.grid(row=2, column=1)

        self.search_button = tk.Button(root, text="Search", command=self.search_account)
        self.search_button.grid(row=3, column=0, columnspan=2)

        self.create_button = tk.Button(root, text="Create Account", command=self.create_account)
        self.create_button.grid(row=4, column=0, columnspan=2)

        # Transaction Section (hidden initially)
        self.transaction_frame = tk.Frame(root)

        self.transaction_label = tk.Label(self.transaction_frame, text="Choose Transaction:")
        self.transaction_label.grid(row=0, column=0, columnspan=2)

        # Use IntVar to track selected radio button
        self.transaction_type_var = tk.IntVar()

        self.deposit_radio = tk.Radiobutton(self.transaction_frame, text="Deposit", value=1, variable=self.transaction_type_var)
        self.deposit_radio.grid(row=1, column=0)

        self.withdraw_radio = tk.Radiobutton(self.transaction_frame, text="Withdraw", value=2, variable=self.transaction_type_var)
        self.withdraw_radio.grid(row=1, column=1)

        self.amount_label = tk.Label(self.transaction_frame, text="Amount:")
        self.amount_label.grid(row=2, column=0)

        self.amount_entry = tk.Entry(self.transaction_frame)
        self.amount_entry.grid(row=2, column=1)

        self.balance_label = tk.Label(self.transaction_frame, text="Account Balance: $0.00")
        self.balance_label.grid(row=3, column=0, columnspan=2)

        # Enter and Exit buttons
        self.enter_exit_button = tk.Button(self.transaction_frame, text="Enter", command=self.execute_transaction)
        self.enter_exit_button.grid(row=4, column=0)

        self.exit_button = tk.Button(self.transaction_frame, text="Exit", command=self.exit_application)
        self.exit_button.grid(row=4, column=1)

    def search_account(self):
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        pin = self.pin_entry.get()

        if not first_name or not last_name or not pin:
            messagebox.showerror("Input Error", "Please fill in all fields.")
            return

        name = f"{first_name} {last_name}"

        # Try to load the account from a file
        self.account = Account.load(name)

        if self.account and self.account.pin == pin:
            self.show_transaction_options()
        else:
            messagebox.showerror("Account Not Found", "Invalid account name or PIN.")
            self.account = None

    def create_account(self):
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        pin = self.pin_entry.get()

        if not first_name or not last_name or not pin:
            messagebox.showerror("Input Error", "Please fill in all fields.")
            return

        name = f"{first_name} {last_name}"

        # Check if account already exists
        if os.path.exists(f"{name}.pkl"):
            messagebox.showerror("Account Exists", f"An account for {name} already exists.")
            return

        # Create and save a new account
        self.account = Account(name, pin)
        self.account.save()

        messagebox.showinfo("Account Created", f"Account created for {name}. You can now log in.")

    def show_transaction_options(self):
        # Hide login UI and show transaction options
        self.first_name_label.grid_forget()
        self.first_name_entry.grid_forget()
        self.last_name_label.grid_forget()
        self.last_name_entry.grid_forget()
        self.pin_label.grid_forget()
        self.pin_entry.grid_forget()
        self.search_button.grid_forget()
        self.create_button.grid_forget()

        self.transaction_frame.grid(row=0, column=0, columnspan=2)
        self.balance_label.config(text=f"Account Balance: ${self.account.get_balance():.2f}")

    def execute_transaction(self):
        # Validate the amount
        try:
            amount = float(self.amount_entry.get())
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid amount.")
            return

        if amount <= 0:
            messagebox.showerror("Input Error", "Amount must be greater than zero.")
            return

        # Check if Deposit or Withdraw is selected
        if self.transaction_type_var.get() == 1:  # Deposit
            if self.account.deposit(amount):
                self.account.save()
                messagebox.showinfo("Success", f"Deposited ${amount:.2f}.")
            else:
                messagebox.showerror("Error", "Deposit failed.")
        elif self.transaction_type_var.get() == 2:  # Withdraw
            if self.account.withdraw(amount):
                self.account.save()
                messagebox.showinfo("Success", f"Withdrew ${amount:.2f}.")
            else:
                messagebox.showerror("Error", "Insufficient funds or invalid amount.")
        else:
            messagebox.showerror("Input Error", "Please select a transaction type.")

        self.balance_label.config(text=f"Account Balance: ${self.account.get_balance():.2f}")

        # Clear the amount field
        self.amount_entry.delete(0, tk.END)

    def exit_application(self):
        # Close the application
        self.root.quit()

