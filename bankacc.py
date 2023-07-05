class BankAccount:
    def __init__(self, first, last, balance):
        self.first = first
        self.last = last
        self.balance = balance
    def balance_inquiry(self):
        print(self.first + " " + self.last + ": " + str(self.balance))

    def withdrawal(self, subMoney):
        self.balance -= subMoney

    def deposit(self,  addMoney):
        self.balance += addMoney

shwetaAcc = BankAccount("Shweta", "Mazalkar", 60000)
shwetaAcc.deposit(5000)
shwetaAcc.withdrawal(300)
shwetaAcc.balance_inquiry()



