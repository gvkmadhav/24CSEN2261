#chat gpt AI
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class InsufficientFundsError(Exception):
    """Custom exception for insufficient funds."""
    pass

class BankAccount:
    def __init__(self, account_holder, balance=0):
        self.account_holder = account_holder
        self.balance = balance
        logging.info(f"Account created for {self.account_holder} with initial balance of ${self.balance}")

    def deposit(self, amount):
        """Deposit money into the account."""
        if amount <= 0:
            logging.error("Deposit amount must be greater than zero.")
            raise ValueError("Deposit amount must be greater than zero.")
        self.balance += amount
        logging.info(f"${amount} deposited. New balance: ${self.balance}")

    def withdraw(self, amount):
        """Withdraw money from the account."""
        if amount <= 0:
            logging.error("Withdrawal amount must be greater than zero.")
            raise ValueError("Withdrawal amount must be greater than zero.")
        if amount > self.balance:
            logging.warning("Attempted to withdraw more than balance.")
            raise InsufficientFundsError("Insufficient funds for this withdrawal.")
        self.balance -= amount
        logging.info(f"${amount} withdrawn. New balance: ${self.balance}")

    def get_balance(self):
        """Return the current balance."""
        return self.balance

    def __str__(self):
        return f"Account holder: {self.account_holder}\nBalance: ${self.balance}"

def main():
    # Example of creating a bank account
    try:
        account = BankAccount("John Doe", 500)
        print(account)

        # Performing some transactions
        account.deposit(200)
        account.withdraw(100)
        account.withdraw(700)  # This will raise an exception

    except InsufficientFundsError as e:
        logging.error(f"Transaction failed: {e}")
    except ValueError as e:
        logging.error(f"Invalid input: {e}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()
