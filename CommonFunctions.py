import DB
import logs
import MyConstants
import popups
import re
from passlib.hash import pbkdf2_sha256


def getSelectedRow(object):
    return object.tableWidget_bills.currentRow()


def getSelectedRows(object):
    return object.tableWidget_Cart.currentRow()


def allOrSpecificBills(list):
    if not len(list):
        return DB.dB.selectSpecificColumnsFromTable((MyConstants.chosenColumnsOfSales), 'sales')
    else:
        return list


def allOrSpecificExpenses(list):
    if not len(list):
        return DB.dB.selectAllFrom('expenses')
    else:
        return list


def calculateExpenses(expensesDate=[]):
    expenses = 0
    for record in expensesDate:
        expenses += record[2]
    return expenses


def calculateIncome(salesDate=[]):
    totalIncome = 0
    pureTotal = 0
    for item in salesDate:
        reuslt = DB.dB.selectByID('sales', item[0])
        reuslt = reuslt[0]
        totalIncome += reuslt[3]-reuslt[5]-reuslt[7]
        pureTotal += reuslt[4]
    return totalIncome, pureTotal


# Users

def checkIfVailed(name='as', password='as', passwordRepeat='as',):
    if name.strip(" ") != "" and password.strip(" ") != "" and passwordRepeat.strip(" ") != "":
        if password == passwordRepeat:
            return True
        else:
            popups.showMessage("اعادة المحاولة", 'كلمة المرور غير متطابقة')
            return False
    else:
        popups.showMessage("خطا", "يرجى ادخال اسم وكلمة مرور")
        return False



def isNew(user):
    result = DB.dB.selectByName('users', user)
    if len(result):
        return False
    else:
        return True


def updateSelector(new, default):
    if isEmpty(new):
        return default
    else:
        return new


def isEmpty(word):
    if word.strip(" ") == "":
        return True
    else:
        return False


def validate(password):
    if len(password) < 8:
        popups.showMessage("خطأ ", "الرجاء التاكد من ان كلمة المرور اكثر من 8 احرف")
    elif re.search('[0-9]', password) is None:
        popups.showMessage("خطأ ", "لابد من وجودرقم واحد على الاقل")
    elif re.search('[A-Z]', password) is None:
        popups.showMessage("خطأ", "لابد من وجود حرف Capital بداخل كلمة المرور A-Z")
    else:
        return True

def checkPassword(user, password, result):
    if user.strip(" ") != "" and password.strip(" ") != "":
            if len(result):
                if pbkdf2_sha256.verify(password, result[0][2]):
                    return True
                else:
                    popups.showMessage("خطأ!", "خطا فى كلمة المرور")
            else:
                popups.showMessage("خطا!", "هذا الاسم غير موجود")
    else:
        popups.showMessage("نقص!", "الرجاء ادخال الباينات كاملة")