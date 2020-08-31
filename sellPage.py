from PyQt5 import uic
from PyQt5.uic.properties import QtWidgets
from PyQt5.QtWidgets import *

import DB
import MyConstants
import CommonFunctions
import popups
import datetime
import users

global userName
class SellPage(QMainWindow):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        uic.loadUi('sell.ui', self)

        # Vars

        self.itemID = None
        self.cartItemID = None
        self.itemSelected = None
        self.itemsInCart = []
        self.totalPrice = None
        self.totalPurePrice = None
        self.discount = 0
        self.payed = 0

        #  Initalize

        self.items = DB.dB.selectAllButId(MyConstants.selectAllItems)
        self.tableWidget.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tableWidget_Cart.setEditTriggers(QTableWidget.NoEditTriggers)

        #  Connect To Func
        self.tableWidget_Cart.itemSelectionChanged.connect(self.cartSelectionChanged)
        self.tableWidget.itemSelectionChanged.connect(self.selectionDBChanged)
        self.pushButton_addToCart.clicked.connect(self.AddToCart)
        self.pushButton_deleteFromCart.clicked.connect(self.removeItem)
        self.pushButton_clearCart.clicked.connect(self.clearCart)
        self.lineEdit_Payed.textChanged.connect(self.changePayed)
        self.lineEdit_DisCount.textChanged.connect(self.changeDiscount)
        self.pushButton_Expenses.clicked.connect(self.addToExpenses)
        self.pushButton_submit.clicked.connect(self.newBill)
        self.refreshTable()

    def AddToCart(self):
        if self.itemSelected is not None:
            if self.itemSelected[4] >= 1:  # self.itemsSelected[4] is quantity
                if not self.inCart(self.itemSelected):
                    item = (self.itemSelected[0], self.itemSelected[1], self.itemSelected[2], 1)
                    self.itemsInCart.append(item)
                    self.refreshCart()
                elif self.inCart(self.itemSelected):
                    copyOfItemSlected=self.itemSelected
                    dialog = popups.MoreItems(self, copyOfItemSlected[4])
                    dialog.lineEdit_Ava.setText(str(copyOfItemSlected[4]))  # Total in Store

                    dialog.show()
                    res = dialog.exec_()
                    if res == dialog.Accepted:
                        try:
                            itemQuantity = int(dialog.horizontalSlider.value())
                            self.removeFromCart(copyOfItemSlected[0])
                            item = (copyOfItemSlected[0], copyOfItemSlected[1], copyOfItemSlected[2], itemQuantity)
                            self.itemsInCart.append(item)
                            self.refreshCart()
                        except:
                            pass
                    else:
                        pass


            else:
                popups.showMessage('خطا', 'لايمكن اضافة هذه القطعة')

        else:
            popups.showMessage('خطأ', 'الرجاء اختيار قطعة لاضافتها للعربة')

    def removeItem(self):
        self.removeFromCart(self.cartItemID)
        self.refreshCart()

    def removeFromCart(self, id):
        for item in self.itemsInCart:
            if item[0] == int(id):
                self.itemsInCart.remove(item)

    def inCart(self, itemSelected):
        for item in self.itemsInCart:
            if itemSelected[0] == item[0]:
                return True
        return False

    def selectionDBChanged(self):
        try:
            self.itemID = self.tableWidget.item(self.getSelectedRow(), 0).text()
            self.changeSelectedItem()
        except Exception as e:
            print(e)

    def getSelectedRow(self):
        return self.tableWidget.currentRow()

    def getSelectedRowCart(self):
        return self.tableWidget_Cart.currentRow()

    def cartSelectionChanged(self):
        try:
            self.cartItemID = self.tableWidget_Cart.item(self.getSelectedRowCart(), 0).text()
        except Exception as e:
            print(e)

    def clearCart(self):
        try:
            self.itemsInCart.clear()
            self.clearSelected()
            self.refreshCart()
        except Exception as e:
            print(e)

    def clearSelected(self):
        self.itemID = None
        self.itemSelected = None
        self.cartItemID = None
        self.discount = 0
        self.payed = 0
        self.totalPurePrice = 0

    def changeSelectedItem(self):
        result = DB.dB.selectByID('items', self.itemID)
        self.itemSelected = result[0]

    def refreshTable(self, items=[]):
        self.tableWidget.clearSelection()
        self.tableWidget.setRowCount(0);
        if not len(items):
            self.items = DB.dB.selectAllButId(MyConstants.selectAllItems)
        else:
            self.items = items
        for row_number, item in enumerate(self.items):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(item):
                cell = QTableWidgetItem(str(data))
                self.tableWidget.setItem(row_number, column_number, cell)

    def refreshCart(self):
        self.tableWidget_Cart.clearSelection()
        self.tableWidget_Cart.setRowCount(0);

        for row_number, item in enumerate(self.itemsInCart):
            self.tableWidget_Cart.insertRow(row_number)
            for column_number, data in enumerate(item):
                cell = QTableWidgetItem(str(data))
                self.tableWidget_Cart.setItem(row_number, column_number, cell)
        self.calcualeTotal()

    def calcualeTotal(self):
        self.totalPrice = 0
        self.totalPurePrice = 0
        for item in self.itemsInCart:
            self.totalPrice += item[2] * item[3]  # price * Qnt
            result = DB.dB.selectByID('items', item[0])
            self.totalPurePrice += result[0][3] * item[3]
        self.lineEdit_Total.setText(str("{:,.2f} EGP".format(self.totalPrice - self.discount)))
        self.remaining()

    def changePayed(self):
        try:
            self.payed = abs(float(self.lineEdit_Payed.text()))
            self.remaining()
        except Exception as e:
            self.lineEdit_Payed.clear()

    def changeDiscount(self):
        try:
            self.discount = abs(float(self.lineEdit_DisCount.text()))
            self.calcualeTotal()
        except Exception as e:
            self.lineEdit_DisCount.clear()

    def remaining(self):
        required = self.totalPrice - self.discount
        remaining = self.payed - required
        self.lineEdit_Left.setText(str("{:,.2f} EGP".format(remaining)))

    def clearLineEdit(self):
        self.lineEdit_Payed.clear()
        self.lineEdit_DisCount.clear()
        self.lineEdit_PhoneNumber.clear()
        self.lineEdit_Left.clear()
        self.lineEdit_Note.clear()
        self.lineEdit_Total.clear()

    def addToExpenses(self):
        try:
            date = datetime.datetime.now()
            amount = float(self.lineEdit_ExpensesAmount.text())
            note = self.lineEdit_Expenses.text()
            try:
                time = str(date.hour) + ':' + str(date.minute) + ':' + str(date.second)
                user =users.User.returnUserName(users.User)
                expense = (user, amount, time, note)
                DB.dB.insertInto(expense, MyConstants.insertExpenses)
                popups.showMessage('تم', 'تم تسجيل العملية')
                self.lineEdit_ExpensesAmount.clear()
                self.lineEdit_Expenses.clear()

            except Exception as e:
                print(e)
        except Exception as e:
            self.lineEdit_ExpensesAmount.clear()
            popups.showMessage("خطا", "الرجاء ادخال رقم فى خانى المبلغ")

    def newBill(self):
        try:
            if len(self.itemsInCart):
                date = datetime.datetime.now()
                time = str(date.hour) + ':' + str(date.minute) + ':' + str(date.second)
                note = self.lineEdit_Note.text()
                phoneNumber = self.lineEdit_PhoneNumber.text()
                user = users.User.returnUserName(users.User)
                returns=0
                # (user,phone,total,pureTotal,discount,date,time,note)
                bill = (user, phoneNumber, self.totalPrice, self.totalPurePrice, self.discount,returns, time, note)
                id = DB.dB.insertInto(bill, MyConstants.insertSales)
                for item in self.itemsInCart:
                    b = DB.dB.selectByID('items', item[0])
                    DB.dB.updateByID('items', (b[0][4] - item[3], b[0][0]))  # b[0][4] is qnt b[0][0] item id
                    billD = (id, item[1], item[2], b[0][3],item[3])  # [1] bill name, [2] price, [3] qnt , b[0][3] real price
                    # purePrice
                    DB.dB.insertInto(billD, MyConstants.insertBill)
                popups.showMessage('تم', 'تم')
                self.itemsInCart.clear()
                self.refreshCart()
                self.refreshTable()
                self.clearLineEdit()
                self.clearSelected()
            else:
                popups.showMessage('خطأ', 'لا يوجد قطع فى العربة')
        except Exception as e:
            print(e)
