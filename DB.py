# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 03:55:32 2020

@author: JC00PER
"""
import sqlite3
import MyConstants
from sqlite3 import Error
import datetime

from passlib.hash import pbkdf2_sha256


def combine(columns, table):
    s = 'SELECT '
    for column in columns:
        s += column
        s += ' ,'
    s = s[0:-1]
    sql = "FROM (%s) " % table
    return s + sql


class DBModifer:

    def __init__(self, name=None):
        self.conn = None
        self.cursor = None

        if name:
            self.open(name)

    def open(self, name):
        try:
            self.conn = sqlite3.connect(name)
            self.cursor = self.conn.cursor()
        except Error as e:
            print(e)

    def table(self, TableConfig):
        try:
            c = self.cursor
            c.execute(TableConfig)
        except Error as e:
            print(e)

    def selectQuery(self, query):
        c = self.cursor
        c.execute(query)
        return c.fetchall()

    def insertInto(self, row, query):
        c = self.cursor
        c.execute(query, row)
        self.conn.commit()
        return c.lastrowid

    def updateTo(self, row, query):
        c = self.cursor
        c.execute(query, row)
        self.conn.commit()

    def selectAllFrom(self, table):
        sql = 'SELECT * FROM (%s)' % table
        c = self.cursor
        c.execute(sql)
        return c.fetchall()

    def selectAlike(self, table,text):
        sql = 'SELECT * FROM (%s) ' % table
        sentence='Where name like "%s" ' % text
        sql =sql+sentence
        c = self.cursor
        c.execute(sql)
        return c.fetchall()


    def selectByName(self, table, name):
        sql = "SELECT * FROM (%s) WHERE name=?" % table
        c = self.cursor
        c.execute(sql, (name,))
        return c.fetchall()

    def selectByID(self, table, itemId):
        sql = "SELECT * FROM (%s) WHERE id=?" % table
        c = self.cursor
        c.execute(sql, (itemId,))
        return c.fetchall()

    def selectAllButId(self, query):
        c = self.cursor
        c.execute(query)
        return c.fetchall()

    def deleteByIdFrom(self, table, id):
        sql = "DELETE FROM %s WHERE id=?" % table
        c = self.cursor
        c.execute(sql, (id,))
        self.conn.commit()

    def deleteByNameFrom(self, table, name):
        c = self.cursor
        sql = 'DELETE FROM %s WHERE name=?' % table
        c.execute(sql, (name,))
        self.conn.commit()

    def clearTable(self, table):
        c = self.cursor
        sql = 'DELETE FROM %s' % table
        c.execute(sql)
        self.conn.commit()

    def updateByID(self, table, item):
        c = self.cursor
        sql = 'Update %s set stock=? where id=?' % table
        c.execute(sql, item)
        self.conn.commit()

    def dropTable(self, table):
        c = self.cursor
        sql = 'drop table if EXISTS %s ' % table
        c.execute(sql)
        self.conn.commit()

    def selectByDate(self, table, date):
        sql = "SELECT * FROM (%s) WHERE date=?" % table
        c = self.cursor
        c.execute(sql, (date,))
        return c.fetchall()

    def selectInterval(self, table, date):
        sql = "SELECT * FROM (%s) WHERE (date >= ? AND date<= ?)" % table
        c = self.cursor
        c.execute(sql, date)
        return c.fetchall()

    def selectSpecificColumnsFromTable(self, columns, table):
        sql = combine(columns,table)
        c = self.cursor
        c.execute(sql)
        return c.fetchall()

    def selectSpecificColumnsFromTableByID(self, columns, table, id):
        sql = combine(columns,table) +'Where id = (%s)' % id
        c = self.cursor
        c.execute(sql)
        return c.fetchall()

    def isDub(self, name):
        users = self.selectByName('users', name)
        if len(users) != 0:
            return True
        return False

    def selectIntervalAndColumns(self, table,columns ,date):
        sql=combine(columns,table) +"WHERE (date >= ? AND date<= ?)"
        c = self.cursor
        c.execute(sql, date)
        return c.fetchall()


dB = DBModifer(MyConstants.database)
#dB.dropTable('sales')
#dB.dropTable('bills')
#dB.dropTable('expenses')
dB.table(MyConstants.sql_create_later_table)
dB.table(MyConstants.sql_create_items_table)
dB.table(MyConstants.sql_create_users_table)
dB.table(MyConstants.sql_create_expenses_table)
dB.table(MyConstants.sql_create_bills_table)
dB.table(MyConstants.sql_create_sales_table)


if not dB.isDub('Hossam'):
    dB.insertInto(('Hossam', pbkdf2_sha256.hash('Hossam'), 1), MyConstants.insertUsers)
