Account_Holders = {
    "Amit": 10000,
    "Bina": 2000,
    "Chetan": 4000,
    "Deepa": 3000,
    "Esha": 5000,
    "Farhan": 7000,
    "Gita": 6000,
    "Hari": 8000,
    "Isha": 9000,
    "Jay": 1000,
    "Kiran": 2500,
    "Lata": 3500,
    "Mohan": 4500,
    "Nina": 1500,
    "Om": 1200,
    "Pooja": 2200,
    "Ravi": 1800,
    "Sara": 2700,
    "Tina": 3200
}

class Bankaccount:
    """This class contains the information about the bank account"""

    def __init__(self,name: str, balance: float):
        self.name = name
        self.balance = balance

    def deposit(self,amount: float) -> float:
        """Add the amount into the balance"""
        if amount <= 0.0:
            raise ValueError("The amount must be positive.")
        else:
            self.balance += amount
        return self.balance

    def withdrawal(self, money_withdrawal: float) -> float:
        """withdrawal the amount from the balance"""
        if money_withdrawal < 0.0:
            raise Exception("Improper amount.")
        elif money_withdrawal <= self.balance:
            self.balance -= money_withdrawal          
        else:
            raise ValueError("Insufficient Balance.")
        return self.balance

    
    def check_balance(self):
        """The current balance"""
        print(f"updated balance ₹{self.balance}")

Account_Holder_Username = input("Enter the name of the Account Holder: ")

# Check if Person exists
if Account_Holder_Username not in Account_Holders:
    print(f"{Account_Holder_Username} is not in the list.")
    exit()

#Account Balance
Account_Balance = Account_Holders[Account_Holder_Username]
print(f"The account balance is ₹{Account_Balance}")

try:
    person1 = Bankaccount(Account_Holder_Username,Account_Balance)

    Deposit_Amount = int(input("Enter the amount you want to deposit: ₹"))
    new_balance = person1.deposit(Deposit_Amount)
    print(f"Balance after deposit: ₹{new_balance}")

    withdrawal_Amount = int(input("Enter the amount you want to withdrawal: ₹"))
    new_balance = person1.withdrawal(withdrawal_Amount)
    print(f"Balance after withdrawl: ₹{withdrawal_Amount}")
    
except Exception as e:
    print(f"Error{e}")
finally:
    print("Your Session is over.")
