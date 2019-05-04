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
    cursor.execute(sql, (firstName, lastName, dob, state))
    db.commit()

def createAccount(customer_id,account_type):
    sql = """ INSERT INTO account (CUSTOMER_ID, ACCOUNT_TYPE) VALUES (%s, %s)"""
    cursor.execute(sql, (customer_id,account_type))
    db.commit()

#def performTx(customer_id, account_id):


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
