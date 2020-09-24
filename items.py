from PyQt5 import uic
from PyQt5.uic.properties import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import resourceFiles_rc
import DB
import MyConstants
import popups



def isEmpty(word):
    if word.strip(" ") == "":
        return True
    else:
        return False


def isVaild(word, flag=False, wtype=str):
    if flag:
        try:
            val = wtype(word)
            return True
        except Exception as e:
            return False
    return True

class Items(QMainWindow):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        uic.loadUi('resources\\items.ui', self)
        # Vars
        self.itemName = None
        self.itemID = None
        self.itemPrice = None
        self.itemQuantity = None
        self.itemPurePrice = None
        self.items = DB.dB.selectAllFrom('items')
        self.refreshTable()
        #  Signals
        self.pushButton.clicked.connect(self.addClicked)
        self.pushButton_Delete.clicked.connect(self.delClicked)
        self.pushButton_Update.clicked.connect(self.updateClicked)
        self.pushButton_clear.clicked.connect(self.clearClicked)
        self.pushButton_refill.clicked.connect(self.refillClicked)
        self.tableWidget.setEditTriggers(QTableWidget.NoEditTriggers)
        self.lineEdit_Name.textChanged.connect(self.nameTextChanged)
        # self.lineEdit_ID.textChanged.connect(self.idTextChanged)
        self.tableWidget.itemSelectionChanged.connect(self.selectionChanged)


    def refreshTable(self, items=[]):
        self.tableWidget.clearSelection()
        self.tableWidget.setRowCount(0);
        if not len(items):
            self.items = DB.dB.selectAllFrom('items')
        else:
            self.items = items
        for row_number, item in enumerate(self.items):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(item):
                cell = QTableWidgetItem(str(data))
                self.tableWidget.setItem(row_number, column_number, cell)

    def addClicked(self):
        self.getInput()
        if not isEmpty(self.itemName) and isVaild(self.itemName, False, str):
            if not isEmpty(self.itemPrice) and isVaild(self.itemPrice, True, float):
                if not isEmpty(self.itemPurePrice) and isVaild(self.itemPurePrice, True, float):
                    if not isEmpty(self.itemQuantity) and isVaild(self.itemQuantity, True, int):
                        item = (self.itemName, float(self.itemPrice), float(self.itemPurePrice), int(self.itemQuantity))
                        # if not self.isDub(item):
                        DB.dB.insertInto(item, MyConstants.insertItems)
                        self.refreshTable()
                        self.resetLineEdit()
                        self.restVars()
                        # else:
                        # self.showMessage("خطا!", "هذه القطعة موجوده سابقا!ّ")
                    else:
                        popups.showMessage("خطا", "الرجاء ادخال رقم فى الخانة المخصصة للكمية")
                else:
                    popups.showMessage('خطا', 'الرجاء ادخال رقم فى خانة سعر الجملة')
            else:
                popups.showMessage("خطا", "الرجاء ادخال رقم فى الخانة المخصصة للسعر")
        else:
            popups.showMessage("خطا", "الرجاء ادخال اسم فى الخانة المخصصة للاسم")


    def delClicked(self):
        try:
            self.getInput()
            if isVaild(self.itemID, True, int):
                DB.dB.deleteByIdFrom('items', self.itemID)
                self.refreshTable()
                self.resetLineEdit()
                self.restVars()
            else:
                popups.showMessage("خطا", "الرجاء ادخال الكود لمسح قطعة")
        except:
            pass

    def updateClicked(self):
        try:
            self.getInput()
            if isVaild(self.itemID, True, int):
                result = DB.dB.selectByID('items', int(self.itemID))
                if len(result):
                    defaultName = result[0][1]
                    defaultPrice = result[0][2]
                    defaultpurePrice = result[0][3]
                    defaultQuantity = result[0][4]
                    self.itemName = self.updateSelector(self.itemName, defaultName)
                    self.itemPrice = self.updateSelector(self.itemPrice, defaultPrice)
                    self.itemQuantity = self.updateSelector(self.itemQuantity, defaultQuantity)
                    self.itemPurePrice = self.updateSelector(self.itemPurePrice, defaultpurePrice)
                    if isVaild(self.itemName, False, str):
                        if isVaild(self.itemPrice, True, float):
                            if isVaild(self.itemPurePrice, True, float):
                                if isVaild(self.itemQuantity, True, int):
                                    item = (self.itemName, float(self.itemPrice), float(self.itemPurePrice),
                                            int(self.itemQuantity),
                                            int(self.itemID))
                                    try:
                                        DB.dB.updateTo(item, MyConstants.updateItem)
                                        self.refreshTable()
                                        self.resetLineEdit()
                                        self.restVars()
                                    except:
                                        popups.showMessage("خطا!", "هذه القطعة موجوده سابقا!ّ")  #
                                else:
                                    popups.showMessage("خطا", "الرجاء ادخال رقم فى الخانة المخصصة للكمية")
                            else:
                                popups.showMessage('خطا', 'الرجاء ادخال رقم فى خانة سعر الجملة')
                        else:
                            popups.showMessage("خطا", "الرجاء ادخال رقم فى الخانة المخصصة للسعر")
                    else:
                        popups.showMessage("خطا", "الرجاء ادخال اسم فى الخانة المخصصة للاسم")


                else:
                    popups.showMessage("خطأ", "هذه القطعة غير موجودة")
            else:
                popups.showMessage("خطا", "الرجاء ادخال الكود لتعديل")
        except Exception as e:
            print(e)

    def updateSelector(self, new, default):
        if isEmpty(new):
            return default
        else:
            return new

    def clearClicked(self):
        dialog=popups.Confirmation(self,'ان تمسح كل الباينات :')
        dialog.show()
        res=dialog.exec_()
        if res==dialog.Accepted:
            try:
                DB.dB.clearTable('items')
                self.refreshTable()
                self.restVars()
            except:
                pass
        else:
            pass

    def refillClicked(self):
        if self.itemID is not None:
            dialog = popups.Refill(self)
            dialog.show()
            res = dialog.exec_()
            if res==dialog.Accepted:
                quantity=dialog.lineEdit_quantity.text()
                try:
                    if isVaild(quantity, True, int):
                        self.itemQuantity = int(self.itemQuantity) + int(quantity)
                        if self.itemQuantity <= 0:
                            popups.showMessage("خطا", "لا يمكن للكمية ان تكون اقل من او تساوى الصفر")
                            self.itemQuantity = 1
                        item = (self.itemQuantity, self.itemID)
                        DB.dB.updateTo(item, MyConstants.refillItem)
                        self.refreshTable()
                        self.resetLineEdit()
                        self.restVars()
                    else:
                        popups.showMessage('خطا','الرجاء ادخال رقم')
                except Exception as e:
                    print(e)
            else:
                pass
        else:
            popups.showMessage('خطا','الرجاء اختيار قطعة لضافة المذيد منها')

    def nameTextChanged(self,text):
        text = text + '%'
        items = DB.dB.selectAlike('items', text)
        if len(items) == 0:
            items = [('لا يوجد', 'لا يوجد', 'لا يوجد', 'لا يوجد', 'لا يوجد')]
            self.refreshTable(items)
        else:
            self.refreshTable(items)

    def selectionChanged(self):
        try:
            self.itemID = self.tableWidget.item(self.getSelectedRow(), 0).text()
            self.itemName = self.tableWidget.item(self.getSelectedRow(), 1).text()
            self.itemPrice = self.tableWidget.item(self.getSelectedRow(), 2).text()
            self.itemPurePrice = self.tableWidget.item(self.getSelectedRow(), 3).text()
            self.itemQuantity = self.tableWidget.item(self.getSelectedRow(), 4).text()
            self.lineEdit_ID.setText(self.itemID)
        except Exception  as  e:
            print(e)

    def getSelectedRow(self):
        return self.tableWidget.currentRow()

    def getItemId(self):
        return self.tableWidget.item(self.getSelectedRow(), 0).text()

    def getInput(self):
        self.itemName = self.lineEdit_Name.text()
        self.itemPrice = self.lineEdit_Price.text()
        self.itemQuantity = self.lineEdit_Quantity.text()
        self.itemID = self.lineEdit_ID.text()
        self.itemPurePrice = self.lineEdit_purePrice.text()

    def resetLineEdit(self):
        self.lineEdit_Name.clear()
        self.lineEdit_Price.clear()
        self.lineEdit_Quantity.clear()
        self.lineEdit_ID.clear()
        self.lineEdit_purePrice.clear()
    def restVars(self):
        self.itemID = None
        self.itemPurePrice = None
        self.itemPrice = None
        self.itemName = None
        self.itemQuantity = None

