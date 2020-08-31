import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget, QVBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from PyQt5.uic.properties import QtCore

import items
import returns
import sellPage
import logs
import users


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(QMainWindow, self).__init__()
        self.title = 'Casher'
        self.left = 0
        self.top = 0
        self.width = 800
        self.height = 600
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.centerWidget = CenterWidget(self)
        self.setCentralWidget(self.centerWidget)
        self.layout = QVBoxLayout(self)
        self.parent = parent
        self.child = None
        # Logout Button


    def disableTaps(self):
        self.centerWidget.tabs.setTabEnabled(1, False)
        self.centerWidget.tabs.setTabEnabled(4, False)
        self.centerWidget.tabs.setTabEnabled(5, False)

    def enableTaps(self):
        self.centerWidget.tabs.setTabEnabled(1, True)
        self.centerWidget.tabs.setTabEnabled(4, True)
        self.centerWidget.tabs.setTabEnabled(5, True)



class CenterWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        #  tap ini
        self.tabs = QTabWidget()
        self.tabs.currentChanged.connect(self.onChange)
        self.sell = sellPage.SellPage()
        self.logs = logs.Logs()
        self.Items = items.Items()
        self.users = users.Users()
        self.returns = returns.Returns()
        self.later = QWidget()
        self.logout = QWidget()
        # Taps management
        self.tabs.resize(800, 600)
        self.tabs.addTab(self.sell, "عربة التسوق")
        self.tabs.addTab(self.logs, 'سجل الحسابات')
        self.tabs.addTab(self.returns, 'المرتجعات')
        self.tabs.addTab(self.later, 'الأجل')
        self.tabs.addTab(self.Items, 'الاصناف')
        self.tabs.addTab(self.users, 'المستخدمين')
        self.tabs.addTab(self.logout, 'تسجيل الخروج')
        # tap icons

        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    #  Taps Customization
    def onChange(self):
        # refreshTables
        self.Items.refreshTable()
        self.sell.refreshTable()
        self.logs.refreshAll()
