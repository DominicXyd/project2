import os
import pickle

class Account:
    def __init__(self, name, pin, balance=0):
        self.name = name
        self.pin = pin  # Store the PIN
        self.balance = balance
        self.set_balance(balance)

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            return True
        return False

    def withdraw(self, amount):
        if amount > 0 and amount <= self.balance:
            self.balance -= amount
            return True
        return False

    def get_balance(self):
        return self.balance

    def get_name(self):
        return self.name

    def set_balance(self, value):
        if value < 0:
            self.balance = 0
        else:
            self.balance = value

    def set_name(self, value):
        self.name = value

    def __str__(self):
        return f"Account Name: {self.get_name()}, Account Balance: ${self.get_balance():.2f}"

    # Save the account to a file
    def save(self):
        with open(f"{self.get_name()}.pkl", "wb") as f:
            pickle.dump(self, f)

    # Load the account from a file
    @staticmethod
    def load(name):
        try:
            with open(f"{name}.pkl", "rb") as f:
                return pickle.load(f)
        except FileNotFoundError:
            return None

