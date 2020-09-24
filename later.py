from PyQt5 import uic
from PyQt5.uic.properties import QtWidgets
from PyQt5.QtWidgets import *
import DB


class Later(QMainWindow):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        uic.loadUi('resources//later.ui', self)
        self.refreshTable()
        # Signals
        self.pushButton_delete.clicked.connect(self.deleteRecord)
        self.pushButton_edit.clicked.connect(self.updateRecord)

    def deleteRecord(self):
        pass

    def updateRecord(self):
        pass

    def refreshTable(self):
        self.tableWidget.clearSelection()
        self.tableWidget.setRowCount(0);
        later = DB.dB.selectAllFrom('later')
        for row_number, item in enumerate(later):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(item):
                cell = QTableWidgetItem(str(data))
                self.tableWidget.setItem(row_number, column_number, cell)
