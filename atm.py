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
    #TODO: check if customer_id exists, if not, then ConnectionError
    customerExists = """select * from customer where customer_id = %s"""
    cursor.execute(customerExists,(customer_id))
    result = cursor.rowcount
    if result == 1:
        sql = """ INSERT INTO account (CUSTOMER_ID, ACCOUNT_TYPE) VALUES (%s, %s)"""
        cursor.execute(sql, (customer_id,account_type))
        db.commit()

def customerLogin():
    customerID = input('Enter customer ID: ')
    customerSql = """select * from customer where customer_id = %s """
    cursor.execute(customerSql,(customerID))
    customer = cursor.fetchone()
    #validate pin number
    pin = input('Enter four digit PIN: ')
    tries = 0
    while True:
        if pin == customer[5]:
            print('Login successful!')
            break
        elif tries > 3:
            print('gtfo')
            break
        else:
            pin = input('Incorrect PIN. \nEnter four digit PIN: ')
            tries += 1
    return customer[0]

#available actions: Withdrawal, deposit, check balance


 #customer[0] is the customer ID after login validation
def selectAccount(customer):  #problem here or on line 52
    accountSql = """select * from account where customer_id = %s """
    cursor.execute(accountSql,(customer))
    accounts = cursor.fetchall()
    print('Accounts:')
    for i in range(len(accounts)):
        print('{0}. {1}'.format(i+1, accounts[i][2]))
    selection = int(input('Select account: ')) -1
    print('You selected your {0} account.'.format(accounts[selection][2]))
    return accounts[selection][0]

# def menuSelection():
#     print('Menu\n1. Check Balance\n2. Deposit\n3. Withdrawal\n4. Switch Account')
#     selection = input('Enter selection: ')
#     if selection == 1:

    #SHOULD I GET ACCOUNT CHOICE BEFORE ALL THESE CHOICES?  PROBABLY!

def checkBalance(account):
    try:
        accountBalanceSql = """select account_balance from transaction where account_id = %s order by transaction_id desc """
        cursor.execute(accountBalanceSql,(account))
        balance = cursor.fetchone()
        return balance[0]
    except:
        return 0
    #need to do some kind of query that pulls the max tx ID or sort by tx ID to get most recent Balance


#def performTx():

#def withdrawalTx():

def depositTx():
    depositAmt = input('Enter deposit amount: ')
    depositSql = """ INSERT INTO transaction (account_id,transaction_type,transaction_amt,account_balance)
     VALUES (%s, %s, %s, %s)"""
    newBalance = checkBalance(account) + float(depositAmt)
    cursor.execute(depositSql,(account,'DEPOSIT',depositAmt,newBalance))
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

customer = customerLogin()
account = selectAccount(customer)
print(checkBalance(account))
depositTx()
