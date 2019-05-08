#! /usr/bin/python3
import pymysql
db = pymysql.connect("localhost","administrator","u9rvTvtQHTBy","john_atm" )
cursor = db.cursor()

def createCustomer():
    sql = """ INSERT INTO customer (FIRST_NAME,LAST_NAME,DATE_OF_BIRTH,STATE) VALUES (%s, %s, %s, %s)"""
    firstName = input('Input first name: ')
    lastName = input('Input last name: ')
    dob = input('Input dob, format is YYYY-MM-DD: ')
    state = input('Input state of residence: ')
    pin = '0000'
    cursor.execute(sql, (firstName, lastName, dob, state))
    db.commit()

def createAccount(customer_id,account_type):
    #TODO: check if customer_id exists, if not, then ConnectionError?
    customerExists = """select * from customer where customer_id = %s"""
    cursor.execute(customerExists,(customer_id))
    result = cursor.rowcount
    if result == 1:
        sql = """ INSERT INTO account (CUSTOMER_ID, ACCOUNT_TYPE) VALUES (%s, %s)"""
        cursor.execute(sql, (customer_id,account_type))
        db.commit()

def customerLogin():
    tries = 1
    while True:
        customerID = input('Enter customer ID: ')
        customerSql = """select * from customer where customer_id = %s """
        cursor.execute(customerSql,(customerID))
        customer = cursor.fetchone()
        if customer is not None:
            break
        elif tries > 2:
            raise Exception('Too many attempts')
        else:
            print('Invalid customer ID')
            tries += 1

    pin = input('Enter four digit PIN: ')
    tries = 1
    while True:
        if pin == customer[5]:
            print('Login successful!')
            break
        elif tries > 2:
            raise Exception('Too many attempts')
            break
        else:
            pin = input('Incorrect PIN. \nEnter four digit PIN: ')
            tries += 1
    return customer[0]

 #customer[0] is the customer ID after login validation
def selectAccount(customer):  #problem here or on line 52
    accountSql = """select * from account where customer_id = %s """
    cursor.execute(accountSql,(customer))
    accounts = cursor.fetchall()

    #Display list of accounts
    print('Accounts:')
    for i in range(len(accounts)):
        print('{0}. {1}'.format(i+1, accounts[i][2]))

    #Create list of accounts for input validation
    accountList = []
    for i in range(len(accounts)):
		    accountList.append(accounts[i][0])

    #Get valid account from user
    #TODO this still doesn't show the right message when first attempt is a failure
    selection = 0
    while selection not in accountList:
        while True:
            try:
                selection = int(input('Select account: '))
            except ValueError:
                print("Not a valid account")
                continue
            else:
                break


    selection = int(selection) -1
    print('You selected your {0} account.'.format(accounts[selection][2]))
    return accounts[selection][0]



def checkBalance(account):
    try:
        accountBalanceSql = """select account_balance from transaction where account_id = %s order by transaction_id desc """
        cursor.execute(accountBalanceSql,(account))
        balance = cursor.fetchone()
        return balance[0]
    except:
        return 0
    #need to do some kind of query that pulls the max tx ID or sort by tx ID to get most recent Balance

def depositTx():
    while True:
        depositAmt = input('Enter deposit amount: ')
        if float(depositAmt) <= 0:
            print('Deposit amount must be greater than 0')
        else:
            break
    depositSql = """ INSERT INTO transaction (account_id,transaction_type,transaction_amt,account_balance)
     VALUES (%s, %s, %s, %s)"""
    newBalance = checkBalance(account) + float(depositAmt)
    cursor.execute(depositSql,(account,'DEPOSIT',depositAmt,newBalance))
    db.commit()
    print('Your balance is now {}'.format(newBalance))


def withdrawalTx():
    while True:
        withdrawalAmt = input('Enter withdrawal amount: ')
        if float(withdrawalAmt) <= 0:
            print('Withdrawal amount must be greater than 0')
        elif float(withdrawalAmt) > checkBalance(account):
            print('Not enough available balance')
        else:
            break
    withdrawalAmt = float(withdrawalAmt)*-1
    depositSql = """ INSERT INTO transaction (account_id,transaction_type,transaction_amt,account_balance)
     VALUES (%s, %s, %s, %s)"""
    newBalance = checkBalance(account) + float(withdrawalAmt)
    cursor.execute(depositSql,(account,'WITHDRAWAL',withdrawalAmt,newBalance))
    db.commit()
    print('Your balance is now {}'.format(newBalance))


#def transferTx():

def admin():
    print('Select operation: \n 1: Account Administrator \n 2: Customer Login')
    selection = input('')

    if selection == '1':
        pw = input('Enter admin password: ')
        if pw == 'admin password':
            print('Select operation: \n 1: createCustomer \n 2: createAccount')
            selection = input('')
            if selection == '1':
                createCustomer()
            elif selection == '2':
                createAccount()
        else:
            print('Access denied')
    elif selection == '2':
        print('Work in progress')



def menuSelection():
    customer = customerLogin()
    account = selectAccount(customer)
    print(checkBalance(account))
    while True:
        print('Menu\n1. Check Balance\n2. Deposit\n3. Withdrawal\n4. Switch Account\n5. Exit')
        selection = input('Enter selection: ')
        if int(selection) == 1:
            print('Your account balance is : %s' % checkBalance(account))
        elif int(selection) == 2:
            depositTx()
        elif int(selection) == 3:
            withdrawalTx()
        elif int(selection) == 4:
            account = selectAccount(customer)
        elif int(selection) == 5:
            print('Thank you!')
            break

menuSelection()
