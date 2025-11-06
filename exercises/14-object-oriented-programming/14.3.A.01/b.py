"""
Transferaufgabe 14.3.A.01 - Refactored Version
BankAccount class with deposit, withdraw, and transaction history functionality
"""

import datetime


class BankAccount:
    def __init__(self, account_holder, account_number):
        """Initialize a bank account with holder name and account number."""
        self.account_holder = account_holder
        self.account_number = account_number
        self.balance = 0.0
        self.transactions = []

    def deposit(self, amount):
        """Deposit money into the account."""
        # Convert to float and validate
        deposit_amount = float(amount)
        if deposit_amount <= 0:
            raise ValueError("Deposit amount must be positive")

        self.balance += deposit_amount

        # Record the transaction
        transaction = {
            "amount": deposit_amount,
            "timestamp": datetime.datetime.now(),
            "type": "deposit",
        }
        self.transactions.append(transaction)

        print(f"Successfully deposited €{deposit_amount:.2f}")
        print(f"New balance: €{self.balance:.2f}")

    def withdraw(self, amount):
        """Withdraw money from the account."""
        # Convert to float and validate
        withdraw_amount = float(amount)
        if withdraw_amount <= 0:
            raise ValueError("Withdrawal amount must be positive")

        # Check if sufficient funds
        if withdraw_amount > self.balance:
            raise ValueError("Not enough funds")

        self.balance -= withdraw_amount

        # Record the transaction (negative for withdrawal)
        transaction = {
            "amount": -withdraw_amount,
            "timestamp": datetime.datetime.now(),
            "type": "withdrawal",
        }
        self.transactions.append(transaction)

        print(f"Successfully withdrew €{withdraw_amount:.2f}")
        print(f"New balance: €{self.balance:.2f}")

    def last_transactions(self):
        """Display the last 10 transactions."""
        if not self.transactions:
            print("No transactions to display.")
            return

        print("\n--- Last Transactions (up to 10) ---")
        print(f"Current balance: €{self.balance:.2f}\n")

        # Get last 10 transactions
        recent_transactions = self.transactions[-10:]

        for transaction in recent_transactions:
            timestamp = transaction["timestamp"].strftime("%d.%m.%Y %H:%M:%S")
            amount = transaction["amount"]

            # Format amount with + or - sign
            if amount > 0:
                amount_str = f"+€{amount:.2f}"
            else:
                amount_str = f"-€{abs(amount):.2f}"

            print(f"{timestamp} | {amount_str}")

        print("-" * 40)


def display_menu():
    """Display the user menu."""
    print("\n=== Bank Account Menu ===")
    print("d - Make deposit")
    print("w - Make withdrawal")
    print("v - View last transactions")
    print("b - Check balance")
    print("q - Exit")
    print("=" * 25)


def main():
    """Main program loop."""
    # Create a test account
    account = BankAccount("Max Mustermann", "MM-12345")
    print(f"Welcome, {account.account_holder}!")
    print(f"Account Number: {account.account_number}")

    while True:
        display_menu()
        choice = input("\nSelect your action: ").strip().lower()

        if choice == "d":
            try:
                amount = input("Enter deposit amount (€): ")
                account.deposit(amount)
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "w":
            try:
                amount = input("Enter withdrawal amount (€): ")
                account.withdraw(amount)
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "v":
            account.last_transactions()

        elif choice == "b":
            print(f"\nCurrent balance: €{account.balance:.2f}")

        elif choice == "q":
            print("\nThank you for using our bank system!")
            print("Goodbye!")
            break

        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
