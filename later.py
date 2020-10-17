from PyQt5 import uic
from PyQt5.uic.properties import QtWidgets
from PyQt5.QtWidgets import *
import DB
import popups
import MyConstants
from PyQt5 import QtCore


class Later(QMainWindow):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)

        uic.loadUi('resources//newLater.ui', self)
        self.refreshTable()
        # vars
        self.id = None
        self.total = None
        self.user = None
        self.nameOfBuyer = None
        self.remaining =None
        # Signals
        self.pushButton_delete.clicked.connect(self.deleteRecord)
        self.pushButton_edit.clicked.connect(self.updateRecord)
        self.tableWidget.itemSelectionChanged.connect(self.selectionChange)

    def selectionChange(self):
        self.id = self.tableWidget.item(self.getSelectedRow(), 0).text()
        self.user = self.tableWidget.item(self.getSelectedRow(), 1).text()
        self.nameOfBuyer = self.tableWidget.item(self.getSelectedRow(), 2).text()
        self.total = self.tableWidget.item(self.getSelectedRow(), 3).text()
        self.remaining=self.tableWidget.item(self.getSelectedRow(), 4).text()

    def deleteRecord(self):
        if self.id is not None:
            dialog = popups.Confirmation(self, ' هل انت متاكد  من ان تمسح هذا الصف :')
            dialog.show()
            res = dialog.exec_()
            if res == dialog.Accepted:
                try:
                    DB.dB.resetLaterForSales((0,self.id))
                    self.resetVars()
                    self.refreshTable()
                except:
                    pass
            else:
                pass
        else:
            popups.showMessage("-_-", "اختار صف لمسحه")

    def updateRecord(self):
        if self.id is not None:
            if self.remaining is not None:
                try:
                    self.remaining = self.tableWidget.item(self.getSelectedRow(), 4).text()
                    item = (self.user, self.nameOfBuyer,self.total,self.remaining, self.id)
                    DB.dB.resetLaterForSales((self.remaining,self.id))
                    self.resetVars()
                    self.refreshTable()
                except Exception as e:
                    print(e)
                    popups.showMessage("-_-", "اختار صف لتعديله")
        else:
            popups.showMessage("-_-", "اختار صف لتعديله")

    def resetVars(self):
        self.id = None
        self.user = None
        self.nameOfBuyer = None
        self.remaining = None
        self.user = None

    def refreshTable(self):
        self.tableWidget.clearSelection()
        self.tableWidget.setRowCount(0);
        later = DB.dB.selectSpecificColumnsFromTable(MyConstants.chosenColumnsOfLater,'sales')
        newlist=[]
        for item in later:
            if float(item[4])>0:
                newlist.append(item)
        for row_number, item in enumerate(newlist):
                self.tableWidget.insertRow(row_number)
                for column_number, data in enumerate(item):
                    cell = QTableWidgetItem(str(data))
                    if column_number != 4:
                        cell.setFlags(QtCore.Qt.ItemIsEnabled)
                    self.tableWidget.setItem(row_number, column_number, cell)

    def getSelectedRow(self):
        return self.tableWidget.currentRow()
