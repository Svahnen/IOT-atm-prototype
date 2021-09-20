import json
from datetime import datetime
import sys


currentMenu = "initialMenu"
running = True
currentAccount = None


loggedInMenuLayout = [
    "1. Withdraw",
    "2. Deposit",
    "3. Balance",
    "4. History",
    "5. Logout"
    ]


accountMenuLayout = [
    "1. Create account",
    "2. Login account",
    "3. Quit"
    ]


createAccountMenuLayout = [
    "Enter an account nr, then a password"
    ]


# Future proof function where its possible to connect to a real database
# instead of database.JSON
def readDatabase():
    try:
        readStream = open("database.JSON", "r")
        jsonList = readStream.read()
        readStream.close()
        dataList = json.loads(jsonList) # Convert the json array to a python list
        return dataList
    except:
        sys.exit("An error occurred when trying to open database.JSON")


tempList = readDatabase()


def writeToDatabase():
    try:
        writeStream = open("database.JSON", "w")
        json_string = json.dumps(tempList)
        writeStream.write(json_string)
        writeStream.close()
    except:
        sys.exit("An error occurred when trying to write to database.JSON")


def toDisplay(menu):
    print("-------------------")
    for value in menu:
        print(value)
    print("-------------------")
    print("Select option: ")


def loginMenu():
    loggedIn = False
    while not loggedIn:
        try:
            account = int(input("Enter your account number: "))
            password = input("Enter your account password: ")
            for value in tempList:
                if int(value["account"]) == account and value["password"] == password:
                    print("you have logged in")
                    loggedIn = True
                    return tempList.index(value) # Return account index to be saved
            if not loggedIn:
                print("Wrong password or account does not exist")
        except ValueError:
            print("You need to enter a number")


def transactionHistory():
    for value in tempList[currentAccount]["transactions"]:
        print("-------------------")
        print("Date:", value["date"])
        print("Amount:", value["amount"])


def loggedInMenu():
    while True:
        toDisplay(loggedInMenuLayout)
        selection = input()
        if selection == "1":
            withdraw()
        elif selection == "2":
            deposit()
        elif selection == "3":
            print("Your current balance is:", tempList[currentAccount]["money"])
        elif selection == "4":
            transactionHistory()
        elif selection == "5":
            break
        else:
            print("You need to enter a menu number")


def createAccount():
    while True:
        accountNr = input("Account number: ")
        if accountNr.isdigit():
            wasFree = True
            for value in tempList:
                if value["account"] == accountNr:
                    print("Account number already in use")
                    wasFree = False
            if wasFree:
                accountPassword = input("Account password: ")
                print("Account created")
                break
        else:
            print("The account needs to be a number")
    account = {
        "account": accountNr,
        "password": accountPassword,
        "money": 0,
        "transactions": []
    }
    tempList.append(account)
    writeToDatabase()


def saveTransaction(amount):
    transaction = {
        "date": datetime.today().strftime('%Y-%m-%d'),
        "amount": amount
    }
    tempList[currentAccount]["transactions"].append(transaction)


def withdraw():
    while True:
        print("Your current balance is:", tempList[currentAccount]["money"])
        amount = input("Enter amount to withdraw: ")
        if amount.isdigit():
            if tempList[currentAccount]["money"] - int(amount) >= 0:
                tempList[currentAccount]["money"] = tempList[currentAccount]["money"] - int(amount)
                saveTransaction("-" + amount)
                writeToDatabase()
                print("Your new balance is:", tempList[currentAccount]["money"])
                break
            else:
                print("Amount exceeds current balance")
        else:
            print("You need to enter a positive numer")

def deposit():
    while True:
        print("Your current balance is:", tempList[currentAccount]["money"])
        amount = input("Enter amount to deposit: ")
        if amount.isdigit():
            tempList[currentAccount]["money"] = tempList[currentAccount]["money"] + int(amount)
            saveTransaction("+" + amount)
            writeToDatabase()
            print("Your new balance is:", tempList[currentAccount]["money"])
            break
        else:
            print("You need to enter a positive numer")


while running:
    toDisplay(accountMenuLayout)
    selection = input()
    if selection == "1":
        createAccount()
    elif selection == "2":
        currentAccount = loginMenu() # Save the index of the logged in account
        loggedInMenu()
    elif selection == "3":
        break
    else:
        print("You need to enter a menu number")