import tkinter as tk
from tkinter import ttk
import csv
import os

##Reads data from the account file
class infoLoader():
    def __init__(self, user, passw) -> None:
        self.username = user
        self.password = passw
        # self.logInUser()

    ##validates user is real and username/password is correct
    def logInUser(self):
        with open('accounts.csv', 'r', newline='\n') as csvfile:
            reader = csv.reader(csvfile, delimiter=' ')
            for line in reader:
                self.user = line

                if self.user[0] == self.username:
                    if self.user[1] == self.password:
                        return True
                    else:
                        return False
            return None
            
    ##Validates Pin is so no illegal attempts at withrawing or depositing
    def checkPin(self, user, pin):
        with open('accounts.csv', 'r', newline='\n') as csvfile:
            reader = csv.reader(csvfile, delimiter=' ')
            for line in reader:
                self.user = line
                if(self.user[3] == pin):
                    if(self.user[0] == user):
                        return True
            return False
    
    
    def checkWithdrawBalance(self, user, balance):
        with open('accounts.csv', 'r', newline='\n') as csvfile:
            reader = csv.reader(csvfile, delimiter=' ')
            for line in reader:
                self.user = line
                if(self.user[4] >= balance):
                    if(self.user[0] == user):
                        return True
            return False
        
    
    def getTransactions(self, user):
        transactions = []
        with open('accounts.csv', 'r', newline='\n') as csvfile:
            reader = csv.reader(csvfile, delimiter=' ')
            for line in reader:
                self.user = line
                if(self.user[0] == user):
                    transactions.append(self.user[4])
            return transactions
    
    ##Gets account balance
    def getBalance(self, user):
        with open('accounts.csv', 'r', newline='\n') as csvfile:
            reader = csv.reader(csvfile, delimiter=' ')
            for line in reader:
                self.user = line
                if(self.user[0] == user):
                    return self.user[4]
        return None
    
    ##Gets the index of the line that we want to be changed
    def getChangedLine(self, user):
        with open('accounts.csv', 'r', newline='\n') as csvfile:
            reader = csv.reader(csvfile, delimiter=' ')
            for i, line in enumerate(reader):
                self.user = line
                if(self.user[0] == user):
                    return i

##writes data to account file
class infoWriter():
    def __init__(self, user, passw) -> None:
        self.user = user
        self.passw = passw

    ##Used to add a new row (User Account) to the accounts csv
    def setUpAccount(self, pin, name, balance):
        self.userInfo = [self.user, self.passw, name, pin, balance]
        file_exists = os.path.isfile("accounts.csv")
        with open('accounts.csv', "a" if file_exists else "w", newline='\n') as csvfile:
            writer = csv.writer(csvfile, delimiter=' ')
            writer.writerow(self.userInfo)

    
    def writeTransaction(self, val):
        file_exists = os.path.isfile("transactions.csv")
        with open('transactions.csv', "a" if file_exists else "w", newline='\n') as csvfile:
            writer = csv.writer(csvfile, delimiter=' ')
            writer.writerow([self.user, val])
        
        self.updateBalance(self, val=val)

    ##Used for depositing a certain amount to a user's account
    def updateBalance(self, val):
        one = infoLoader(self.user, passw='n/a')
        line = one.getChangedLine(self.user);

        with open('accounts.csv', "r", newline='\n') as csvfile:
            reader = csv.reader(csvfile, delimiter=' ')
            lines = list(reader) 

        with open('accounts.csv', "w", newline='\n') as csvfile2:
            writer = csv.writer(csvfile2, delimiter=' ')

            for i, row in enumerate(lines):
                if i == line:
                    self.user = row
                    self.user[4] = int(self.user[4]) + int(val)
                    print(self.user)
                    writer.writerow(self.user)        
                else:
                    writer.writerow(row)

    ##Used for withdrawing a certain amount from a user's account, cannot be negative
    def updatewithdrawBalance(self, val):
        one = infoLoader(self.user, passw='n/a')
        line = one.getChangedLine(self.user);

        with open('accounts.csv', "r", newline='\n') as csvfile:
            reader = csv.reader(csvfile, delimiter=' ')
            lines = list(reader) 

        with open('accounts.csv', "w", newline='\n') as csvfile2:
            writer = csv.writer(csvfile2, delimiter=' ')

            for i, row in enumerate(lines):
                if i == line:
                    self.user = row
                    if(int(self.user[4]) > 0):
                        self.user[4] = int(self.user[4]) + (int(val) * -1)
                    else: 
                        self.user[4] = 0
                    print(self.user)
                    writer.writerow(self.user)        
                else:
                    writer.writerow(row)

#Window after a user is logged in
class LogInWindow():
    #name, pin ,user, passw
    def __init__(self, parent, user, passw, name = '99999', pin = 'N/A') -> None:
        ##If no user account found, create a new account
        if(name != '99999'):
            newuser = infoWriter(user=user, passw=passw)
            newuser.setUpAccount(name=name, pin=pin, balance= 0)
            # LogInWindow(parent=parent, user=user, passw=passw)
            # parent.destroy()

        print("In Login", user, passw)
        use = infoLoader(user=user, passw=passw)
        print(use.logInUser())

        ##Checks if there is an account
        if(use.logInUser() == None):
            logInRoot = tk.Tk()
            logInRoot.geometry("700x100")
            self.logInForm = tk.Label(master=logInRoot, text='No User found. Please Create An Account First', font='Calibri 25 bold')
            self.logInForm.pack()
        ##Checks if password is incorrect, but username is correct.
        elif(use.logInUser() == False):
            logInRoot = tk.Tk()
            logInRoot.geometry("700x100")
            self.logInForm = tk.Label(master=logInRoot, text='Wrong Password, Try Again.', font='Calibri 25 bold')
            self.logInForm.pack()
        ##If logged in
        else:
            parent.destroy()
            self.username = user
            self.password = passw
            logInRoot = tk.Tk()
            logInRoot.geometry("800x800")
            self.logInForm = tk.Label(master=logInRoot, text='ACCOUNT INFORMATION', font='Calibri 32 bold')
            self.logInForm.pack()
            self.usernameW = tk.Label(master=logInRoot, text=str('Welcome ' + self.username), font='Calibri 25 bold')
            self.usernameW.pack()
            self.balance = BalanceWindow(parent=logInRoot, user = self.username)
            self.balance.pack()
            self.depositButton = tk.Button(master=logInRoot, text='Deposit Amount', command=lambda: DepositWindow(self.username), width=19, font='Calibri 23')
            self.depositButton.pack()
            self.withdrawButton = tk.Button(master=logInRoot, text='Withdraw Amount', command=lambda: WithdrawWindow(parent=parent, user= self.username), width=19, font='Calibri 23')
            self.withdrawButton.pack()
            self.ExitMenu = tk.Button(master=logInRoot, text='Exit', command= lambda: logInRoot.destroy(), width=19, font='Calibri 23')
            self.ExitMenu.pack()

##Balance widget shown on the logged in page
class BalanceWindow(tk.Frame):
    balance = 0

    def __init__(self, parent, user, *args, **kwargs) -> None:
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        one = infoLoader(user=user, passw='n/a')
        self.balanceForm = tk.Label(master=parent, text=str('Balance: $') + str(one.getBalance(user=user)), font='Calibri 32 bold')
        self.balanceForm.pack()

##Pin window that resitricts users from depositing or withdrawing without a valid pin
class PinWindow():
    pinNum = 0
    def __init__(self, parent, user) -> None:
        # tk.Frame.__init__(self, parent, *args, **kwargs)
        # self.parent = parent
        self.username = user
        self.pinRoot = tk.Tk()
        self.pinRoot.geometry("400x300")
        self.pinForm = tk.Label(master=self.pinRoot, text=str('Enter PIN #: '), font='Calibri 32 bold')
        self.pinForm.pack()
        self.pinEntry = tk.Entry(master=self.pinRoot, textvariable=self.pinNum, font='Calibri 23')
        self.pinEntry.pack()
        self.pinButton = tk.Button(master=self.pinRoot, text='Confirm', command= lambda: self.pinRoot.destroy() if self.checkCurPin() else self.destroyBoth(parent=parent), width=19, font='Calibri 23')
        self.pinButton.pack()

    def checkCurPin(self):
        one = infoLoader(user=self.username, passw="n/a")
        return one.checkPin(user= self.username, pin= self.pinEntry.get())
    
    def destroyBoth(self, parent):
        parent.destroy()
        self.pinRoot.destroy()

##Deposit window
class DepositWindow():
    amount = 0
    def __init__(self, user) -> None:
        self.useer = user
        self.deposit = tk.Tk()
        self.deposit.geometry('700x300')
        PinWindow(parent=self.deposit, user=user)
        self.depositForm = tk.Label(master=self.deposit, text=str('Enter Deposit Amount: '), font='Calibri 24 bold')
        self.depositForm.pack()
        self.depositEntry = tk.Entry(master=self.deposit, textvariable=self.amount, font='Calibri 23')
        self.depositEntry.pack()
        self.depositButton = tk.Button(master=self.deposit, text='Confirm', command= lambda: self.depositAmount(), width=19, font='Calibri 23')
        self.depositButton.pack()

    def depositAmount(self):
        one = infoWriter(self.useer, 'n/a')
        one.updateBalance(self.depositEntry.get())
        self.deposit.destroy()

##Withdraw window
class WithdrawWindow():
    amount = 0
    def __init__(self, parent, user) -> None:
        self.useer = user
        self.deposit = tk.Tk()
        self.deposit.geometry('700x300')
        PinWindow(parent=self.deposit, user=user)
        self.depositForm = tk.Label(master=self.deposit, text=str('Enter Withdraw Amount: '), font='Calibri 24 bold')
        self.depositForm.pack()
        self.depositEntry = tk.Entry(master=self.deposit, textvariable=self.amount, font='Calibri 23')
        self.depositEntry.pack()
        self.depositButton = tk.Button(master=self.deposit, text='Confirm', command= lambda: self.withdrawAmount(), width=19, font='Calibri 23')
        self.depositButton.pack()

    def withdrawAmount(self):
        one = infoWriter(self.useer, 'n/a')
        one.updatewithdrawBalance(self.depositEntry.get())
        self.deposit.destroy()

##Create an account window
class CreateAccountWindow():
    def __init__(self, parent) -> None:
        self.fullName = tk.StringVar()
        self.pinNumber = tk.StringVar()
        self.username = tk.StringVar()
        self.password = tk.StringVar()

        createAccountWindow = tk.Tk()
        createAccountWindow.geometry("800x800")
        parent.destroy()
        self.createAccountForm = tk.Label(master=createAccountWindow, text='Create Account', font='Calibri 32 bold')
        self.createAccountForm.pack()
        self.fullnameLabel = tk.Label(master=createAccountWindow, text='Full Name: ', font='Calibri 23 bold')
        self.fullnameLabel.pack()
        self.fullnameEntry = tk.Entry(master=createAccountWindow, textvariable=self.fullName, font='Calibri 23')
        self.fullnameEntry.pack()
        self.pinLabel = tk.Label(master=createAccountWindow, text='Enter Pin Number: ', font='Calibri 23 bold')
        self.pinLabel.pack()
        self.pinEntry = tk.Entry(master=createAccountWindow, textvariable=self.pinNumber, font='Calibri 23')
        self.pinEntry.pack()
        self.userLabel = tk.Label(master=createAccountWindow, text='Enter Username: ', font='Calibri 23 bold')
        self.userLabel.pack()
        self.userEntry = tk.Entry(master=createAccountWindow, textvariable=self.username, font='Calibri 23')
        self.userEntry.pack()
        self.passLabel = tk.Label(master=createAccountWindow, text='Enter Password: ', font='Calibri 23 bold')
        self.passLabel.pack()
        self.passEntry = tk.Entry(master=createAccountWindow, textvariable=self.password, font='Calibri 23')
        self.passEntry.pack()
        self.CreateAccountButton = tk.Button(master=createAccountWindow, text='Create Account', command=lambda : LogInWindow(createAccountWindow , name= self.fullnameEntry.get(), pin= self.pinEntry.get(), user= self.userEntry.get(), passw= self.passEntry.get()), width=19, font='Calibri 23')
        self.CreateAccountButton.pack()


    def setUserName(self, user):
        if len(user) != 0:
            self.username = user

    def setPassword(self, password):
        if len(password) != 0:
            self.password = password

    def getUserName(self):
        return self.username

##Window to login or sign up
class MenuWindow(tk.Frame):
    def __init__(self, parent, *args, **kwargs) -> None:
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.parent = parent
        self.menuHome = tk.Label(master=parent, text='BANK OF PY', font='Calibri 32 bold')
        self.menuHome.pack()
        self.logInLabel = tk.Label(master=parent, text='Username: ', font='Calibri 23 bold')
        self.logInLabel.pack()
        self.logInEntry = tk.Entry(master=parent, textvariable=self.username, font='Calibri 23')
        self.logInEntry.pack()
        self.passLabel = tk.Label(master=parent, text='Password: ', font='Calibri 23 bold')
        self.passLabel.pack()
        self.passEntry = tk.Entry(master=parent, textvariable=self.password, font='Calibri 23')
        self.passEntry.pack()
        self.LogInButton = tk.Button(master=parent, text='Log In', command=lambda : LogInWindow(parent, user= self.logInEntry.get(), passw= self.passEntry.get()), width=19, font='Calibri 23')
        self.LogInButton.pack()
        self.createAccount = tk.Button(master=parent, text='Create Account', command=lambda : CreateAccountWindow(parent=parent), width=19, font='Calibri 23')
        self.createAccount.pack()
        self.ExitMenu = tk.Button(master=parent, text='Exit', command= lambda: parent.destroy(), width=19, font='Calibri 23')
        self.ExitMenu.pack()

def main():
    root = tk.Tk()
    root.geometry("800x500")
    root.resizable(False, False)
    #Worry about color later
    # root.configure(background='#1A1A1A')
    MenuWindow(root).pack(side="top", fill="both", expand=True)
    root.mainloop()

main()