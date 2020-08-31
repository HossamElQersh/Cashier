# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 03:57:14 2020

@author: hoss_
"""
dateString='date("now")'
database = r"dbase.db"

vKey="MFRPQ-FJQBM-OCMXH-MIYZC"
sql_create_items_table = """ CREATE TABLE IF NOT EXISTS items (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        price real  NOT NULL,
                                        realPrice real NOT NULL,
                                        stock integer NOT NUll
                                    ); """

sql_create_users_table = """CREATE TABLE IF NOT EXISTS users (
                                    id integer PRIMARY KEY,
                                    name text NOT NULL,
                                    password text NOT Null,
                                    admin integer NOT NULL
                                );"""

sql_create_sales_table = """CREATE TABLE IF NOT EXISTS sales (
                                    id integer PRIMARY KEY,
                                    user text,
                                    phone text,
                                    total real,
                                    pureTotal real,
                                    discount real,
                                    returns real,
                                    date text,
                                    time text,
                                    note text 
                                );"""
sql_create_expenses_table="""CREATE TABLE IF NOT EXISTS expenses (
                                    id integer PRIMARY KEY,
                                    user text,
                                    total real,
                                    date text,
                                    time text,
                                    note text 
                                );"""
sql_create_bills_table="""CREATE TABLE IF NOT EXISTS bills (
                                    id integer NOT Null,
                                    item text  NOT Null,
                                    price real NOT Null,
                                    purePrice real NOT Null,
                                    qnt integer NOT Null,
                                    FOREIGN KEY(id) REFERENCES sales(id),
                                    FOREIGN KEY(item) REFERENCES items(name),
                                    PRIMARY KEY(id,item,price)
                                );"""
selectAllItems="select id ,name ,price ,stock from items "
selectByDate="select * from sales where date = ?"
insertItems = ''' INSERT INTO items(name,price,realPrice,stock)
              VALUES(?,?,?,?); '''

insertUsers = ''' INSERT INTO users(name,password,admin)
              VALUES(?,?,?); '''
insertSales = ''' INSERT INTO sales(user,phone,total,pureTotal,discount,returns,date,time,note)
              VALUES(?,?,?,?,?,?,date("now"),?,?); '''
insertExpenses = ''' INSERT INTO expenses(user,total,date,time,note)
              VALUES(?,?,date("now"),?,?); '''
insertBill=''' INSERT INTO bills(id,item,price,purePrice,qnt)
              VALUES(?,?,?,?,?); '''
updateItem = ''' UPDATE items
              SET name = ? ,
                  price = ? ,
                  realPrice=?,
                  stock = ? 
              WHERE id = ?'''
refillItem=''' UPDATE items
              SET stock = ? 
              WHERE id = ?'''
updateUsers=''' UPDATE users
              SET name = ? ,
                  password = ? ,
                  admin = ? 
              WHERE id = ?'''
updateUsersWithoutPasswordChange='''UPDATE users
              SET name = ? ,
                  admin = ? 
              WHERE id = ?'''
updateBills= '''update bills
                set qnt=?
                where (id = ? and item = ? and price = ?)
                '''
updateSales=''' UPDATE sales
              SET total = ? ,
                  pureTotal = ? ,
                  discount = ? ,
                  returns = ?,
                  note = ?
              WHERE id = ?'''


#Vars

chosenColumnsOfSales = ('id', 'user', 'phone', 'total','pureTotal','discount','returns','date', 'time')
userColumns = ('name', 'password', 'admin')
billsColumns=('item', 'price','qnt')
'''
                                    user text,
                                    phone text,
                                    total real,
                                    pureTotal real,
                                    discount real,
                                    returns real,
                                    date text,
                                    time text,
                                    note text '''