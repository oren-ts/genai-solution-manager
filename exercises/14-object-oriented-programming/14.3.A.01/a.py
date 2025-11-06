"""
Transferaufgabe 14.3.A.01
Task (DE):
Task (EN): a) Define a class BankAccount that has attributes for the account holder (inhaber), the account number (konto_nr),
           the current account balance (kontostand), and a list of the last ten transactions (transaktionen). The account balance
           should be initialized with a starting value of 0, and the transaction list should be empty.
           b) Implement a method deposit that accepts an amount and increases the account balance accordingly. The method should
           also store the transaction (date, time, amount) in the transaction list. Use the datetime module to record the current
           date and time.
           c) Implement a method withdraw that accepts an amount and checks whether the amount can be withdrawn from the current
           balance. If yes, the amount should be withdrawn and the transaction stored. If not, an exception with the message
           "Not enough funds" should be thrown.
           d) Add a method last_transactions that displays the last ten transactions.
           e) Create an instance of the BankAccount class for a user and perform several deposits and withdrawals. Use exceptions
           to handle errors like trying to withdraw more money than is available.
           f) Implement a simple console-based user interface that allows the user to make deposits, withdrawals, and view the
           last transactions.
"""

import datetime


class BankAccount:

    def __init__(self, acct_holder, acct_num):
        self.acct_holder = acct_holder
        self.acct_num = acct_num
        self.acct_blnce = 0
        self.acct_transact = []

    def deposit(self, amnt):
        self.acct_blnce += abs(float(amnt))
        current_datetime = datetime.datetime.now()
        transaction_record = {"amount": abs(float(amnt)), "timestamp": current_datetime}
        self.acct_transact.append(transaction_record)

    def withdraw(self, amnt):
        if abs(float(amnt)) <= self.acct_blnce:
            self.acct_blnce -= abs(float(amnt))
            current_datetime = datetime.datetime.now()
            transaction_record = {
                "amount": (-1) * abs(float(amnt)),
                "timestamp": current_datetime,
            }
            self.acct_transact.append(transaction_record)
        else:
            raise ValueError("Not enough funds.")

    def last_transactions(self):
        report = ""
        for transaction in self.acct_transact[-10:]:
            timestamp = transaction["timestamp"].strftime("%d.%m.%Y %H:%M:%S")
            if transaction["amount"] > 0:
                amount = "+" + str(transaction["amount"]) + "€"
            else:
                amount = str(transaction["amount"]) + "€"
            report += timestamp + " " + amount + "\n"
        print(report)


if __name__ == "__main__":
    test_account = BankAccount("Max Mustermann", "MM-12345")
    MENU = """
            d - make deposits
            w - withdrawls
            v - last transactions
            q - exit
            """
    selection = ""
    while selection != "q":
        print(MENU)
        selection = input("Select your action: ").strip().lower()
        if selection == "d":
            try:
                amount = float(input("Enter deposit amount: "))
                test_account.deposit(amount)
            except ValueError:
                print("Inavalid input.")
        elif selection == "w":
            amount = input("Enter withdraw amount: ")
            try:
                test_account.withdraw(amount)
            except ValueError as e:
                print(e)
        elif selection == "v":
            test_account.last_transactions()
        elif selection == "q":
            print("Thanky you and goodbye!")
            break
