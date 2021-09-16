import json

currentMenu = "initialMenu"
running = True

loggedInMenuLayout = [
    "1. Withdraw",
    "2. Deposit",
    "3. Balance",
    "4. Logout"
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
    readStream = open("database.JSON", "r")
    jsonList = readStream.read()
    readStream.close()
    dataList = json.loads(jsonList) # Convert the json array to a python list
    return dataList

tempList = readDatabase()

def writeToDatabase():
    writeStream = open("database.JSON", "w")
    json_string = json.dumps(tempList)
    writeStream.write(json_string)
    writeStream.close()

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
            if not loggedIn:
                print("Wrong account or password")
        except:
            print("You need to enter a number")


def loggedInMenu():
    while True:
        toDisplay(loggedInMenuLayout)
        selection = input()
        if selection == "1":
            break
        elif selection == "2":
            break
        elif selection == "3":
            break
        elif selection == "4":
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


while running:
    toDisplay(accountMenuLayout)
    selection = input()
    if selection == "1":
        #TODO: Create account function that also saves the created account
        createAccount()
    elif selection == "2":
        loginMenu()
        loggedInMenu()
    elif selection == "3":
        break
    else:
        print("You need to enter a menu number")