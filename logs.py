from PyQt5 import uic
from PyQt5.uic.properties import QtWidgets
from PyQt5.QtWidgets import *

import DB
import MyConstants
import CommonFunctions
import datetime
import popups
import resourceFiles_rc


class Logs(QMainWindow):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        uic.loadUi('resources\\logs.ui', self)
        # Vars
        date = datetime.datetime.now()
        self.billID = None
        self.bill = None
        self.expenseID = None
        self.expenses = None
        self.pureProfit = None
        self.cash = None
        self.inCome = None
        self.itemRealPrice = None
        self.detailsOfBill = None
        self.chosenBills = DB.dB.selectSpecificColumnsFromTable((MyConstants.chosenColumnsOfSales), 'sales')

        # ini
        self.tableWidget_bills.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tableWidget_expenses.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tableWidget_billdetail.setEditTriggers(QTableWidget.NoEditTriggers)
        self.dateEdit_from.setDate(date)
        self.dateEdit_to.setDate(date)
        self.tableWidget_expenses.hide()
        #  Connect Functions
        self.pushButton_bills.clicked.connect(self.showBills)
        self.pushButton_expenses.clicked.connect(self.showExpenses)
        self.tableWidget_bills.itemSelectionChanged.connect(self.selectedBillChanged)
        self.dateEdit_from.dateChanged.connect(self.timeFilter)
        self.dateEdit_to.dateChanged.connect(self.timeFilter)
        self.pushButton_all.clicked.connect(self.refreshAll)

        self.refreshAll()

    def refreshAll(self):
        self.refreshBillsTable()
        self.refreshExpensesTable()
        sales=DB.dB.selectSpecificColumnsFromTable((MyConstants.chosenColumnsOfSales), 'sales')
        expenses=DB.dB.selectAllFrom('expenses')
        self.createReports(sales,expenses)

    def showExpenses(self):
        self.tableWidget_bills.hide()
        self.pushButton_expenses.setFlat(True)
        self.pushButton_bills.setFlat(False)
        self.tableWidget_expenses.show()

    def showBills(self):
        self.tableWidget_expenses.hide()
        self.pushButton_bills.setFlat(True)
        self.pushButton_expenses.setFlat(False)
        self.tableWidget_bills.show()

    def refreshBillsTable(self, bills=[], fromFilter=False):
        self.tableWidget_bills.clearSelection()
        self.tableWidget_bills.setRowCount(0);
        if not fromFilter:
            bills = CommonFunctions.allOrSpecificBills(bills)
        for row_number, item in enumerate(bills):
            self.tableWidget_bills.insertRow(row_number)
            for column_number, data in enumerate(item):
                cell = QTableWidgetItem(str(data))
                self.tableWidget_bills.setItem(row_number, column_number, cell)

    def refreshDetailsOfBillsTable(self):
        self.tableWidget_billdetail.clearSelection()
        self.tableWidget_billdetail.setRowCount(0);
        for row_number, item in enumerate(self.detailsOfBill):
            self.tableWidget_billdetail.insertRow(row_number)
            for column_number, data in enumerate(item):
                cell = QTableWidgetItem(str(data))
                self.tableWidget_billdetail.setItem(row_number, column_number, cell)

    def refreshExpensesTable(self, expenses=[], fromFilter=False):
        self.tableWidget_expenses.clearSelection()
        self.tableWidget_expenses.setRowCount(0);
        if not fromFilter:
            expenses = CommonFunctions.allOrSpecificExpenses(expenses)
        for row_number, item in enumerate(expenses):
            self.tableWidget_expenses.insertRow(row_number)
            for column_number, data in enumerate(item):
                cell = QTableWidgetItem(str(data))
                self.tableWidget_expenses.setItem(row_number, column_number, cell)

    def selectedBillChanged(self):
        try:
            self.billID = int(self.tableWidget_bills.item(CommonFunctions.getSelectedRow(self), 0).text())
            self.updateScreen()
        except Exception as e:
            print(e)

    def updateScreen(self):
        self.bill = DB.dB.selectByID('sales', self.billID)
        self.bill = self.bill[0]
        self.detailsOfBill = DB.dB.selectSpecificColumnsFromTableByID(('item', 'price', 'purePrice', 'qnt'), 'bills',
                                                                      self.billID)
        self.refreshDetailsOfBillsTable()
        note = self.bill[9]
        self.lineEdit_note.setText(note)

    def timeFilter(self):
        dateFrom = self.dateEdit_from.dateTime().toString("yyyy-MM-dd")
        dateTo = self.dateEdit_to.dateTime().toString("yyyy-MM-dd")
        if dateFrom > dateTo:
            popups.showMessage('فترة', 'يجب ان تكون بداية الفترة اصغر من نهايتها ')
        date = (dateFrom, dateTo)
        salesData = DB.dB.selectIntervalAndColumns('sales', MyConstants.chosenColumnsOfSales, date)
        expensesData = DB.dB.selectInterval('expenses', date)
        self.refreshBillsTable(salesData, True)
        self.refreshExpensesTable(expensesData, True)
        self.createReports(salesData, expensesData)

    def createReports(self, salesData=[], expensesData=[]):
        self.expenses = CommonFunctions.calculateExpenses(expensesData)
        self.inCome, self.itemRealPrice = CommonFunctions.calculateIncome(salesData)
        self.cash = self.inCome - self.expenses
        self.pureProfit = self.cash - self.itemRealPrice
        self.lineEdit_pureProfit.setText(str(self.pureProfit))
        self.lineEdit_profit.setText(str(self.cash))
        self.lineEdit_expenses.setText(str(self.expenses))
        self.lineEdit_total.setText(str(self.inCome))
