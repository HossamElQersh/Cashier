import re

from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5 import QtCore
import DB
import MyConstants
import popups


class Returns(QMainWindow):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        uic.loadUi('resources//newReturns.ui', self)
        # Vars
        self.billID = None
        self.billAmount = None
        self.discount = None
        self.toReturn = None
        self.bill = None
        self.billSale = None
        self.note = None
        #  Signals
        self.lineEdit_discount.editingFinished.connect(self.discountEdited)
        self.pushButton_search.clicked.connect(self.searchForBill)
        self.tableWidget.cellChanged.connect(self.ChangeValue)
        self.pushButton_returnAll.clicked.connect(self.deleteBill)
        self.pushButton_changeBill.clicked.connect(self.changeBill)

    def deleteBill(self):
        if self.billID is not None:
            tempID = self.billID
            dialog = popups.Confirmation(self, 'ان تمسح الفاتورة :')
            dialog.show()
            res = dialog.exec_()
            if res == dialog.Accepted:
                try:
                    DB.dB.deleteByIdFrom('sales', tempID)
                    DB.dB.deleteByIdFrom('bills', tempID)
                    self.refreshTable([])
                    self.clearVars()
                    popups.showMessage(':)', 'تم مسح الفاتورة')
                except Exception as e:
                    print(e)
            else:
                pass
        else:
            popups.showMessage(":)", 'من فضلك ادخل رقم الفاتورة')

    def changeBill(self):
        if self.billID is not None:
            row = 0
            column = 2
            total = self.calculatePurePrice()
            note = self.note + ' + تم تعديل هذه الفاتورة'
            newBillAmount = self.billAmount - self.toReturn
            newSale = (newBillAmount, total, self.discount, self.toReturn, note, self.billID)
            DB.dB.updateTo(newSale, MyConstants.updateSales)
            for record in self.bill:
                newQnt = int(self.tableWidget.item(row, column).text())
                newbill = (newQnt, self.billID, record[0], record[1])
                DB.dB.updateTo(newbill, MyConstants.updateBills)
                row += 1
            popups.showMessage(':)', '')
        else:
            popups.showMessage(":)", 'من فضلك ادخل رقم الفاتورة')

    def searchForBill(self):
        self.billID = self.lineEdit_id.text()
        if self.billID.strip(' ') != "":
            try:
                self.bill = DB.dB.selectSpecificColumnsFromTableByID(MyConstants.billsColumns, 'bills', self.billID)
                if len(self.bill) != 0:
                    self.refreshTable(self.bill)
                    self.billSale = DB.dB.selectByID('sales', self.billID)
                    self.billAmount = self.billSale[0][3]
                    self.discount = self.billSale[0][5]
                    self.note = self.billSale[0][9]
                    self.updateVars()
                else:
                    popups.showMessage("لايوجد", "هذه الفاتورة غير موجده")
                    self.refreshTable([])
            except Exception as e:
                self.refreshTable([])
                popups.showMessage("رقم الفاتورة", "من فضلك ادخل رقم!! الفاتورة")

    def discountEdited(self):
        text=self.lineEdit_discount.text()
        self.discount=self.billSale[0][5]
        try:
            newDiscount = float(text)
            if newDiscount > self.discount:
                newDiscount = self.billSale[0][5]
                self.lineEdit_discount.setText(str(self.billSale[0][5]))
            self.discount=newDiscount
        except Exception as e:
            self.lineEdit_discount.setText(str('0'))
            self.discount=0

    def updateVars(self):
        self.toReturn = self.calculateTotal()
        self.updateLineEdit()

    def clearVars(self):
        self.billID = 0
        self.billAmount = 0
        self.discount = 0
        self.toReturn = 0
        self.bill = None
        self.billSale = None
        self.updateLineEdit()

    def updateLineEdit(self):
        self.lineEdit_amount.setText(str(self.billAmount))
        self.lineEdit_id.setText(str(self.billID))
        self.lineEdit_discount.setText(str(self.discount))
        self.lineEdit_return.setText(str(self.toReturn))

    def ChangeValue(self, row, column):
        if column == 2:
            try:
                s = int(self.tableWidget.item(row, column).text())
                if s > self.bill[row][column]:
                    self.tableWidget.item(row, column).setText(str(self.bill[row][column]))
                try:
                    self.updateVars()
                except:
                    pass
            except Exception as e:
                self.tableWidget.item(row, column).setText(str(self.bill[row][column]))

    def calculateTotal(self):
        total = 0
        row = 0
        column = 2
        for record in self.bill:
            newQnt = int(self.tableWidget.item(row, column).text())
            price = float(self.tableWidget.item(row, column - 1).text())
            total += (newQnt * price)
            row += 1
        self.toReturn = self.billAmount - total
        return self.toReturn

    def calculatePurePrice(self):
        result = DB.dB.selectByID('bills', self.billID)
        pureTotal = 0
        row = 0
        column = 2
        for bill in result:
            newQnt = int(self.tableWidget.item(row, column).text())
            pureTotal += bill[3] * newQnt
            row += 1
        return pureTotal

    def refreshTable(self, billItems):
        self.tableWidget.clearSelection()
        self.tableWidget.setRowCount(0);
        for row_number, bill in enumerate(billItems):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(bill):
                cell = QTableWidgetItem(str(data))
                if column_number != 2:
                    cell.setFlags(QtCore.Qt.ItemIsEnabled)
                self.tableWidget.setItem(row_number, column_number, cell)
