import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget, QVBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.uic.properties import QtCore, QtGui, QtWidgets

import MyConstants
import items
import returns
import sellPage
import logs
import users
import later

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(QMainWindow, self).__init__(parent)
        uic.loadUi('resources\\mainWindow.ui', self)
        self.title = 'Cashier'
        self.left = 0
        self.top = 0
        self.width = 1320
        self.height = 800
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.centerWidget = CenterWidget(self)
        self.setCentralWidget(self.centerWidget)
        self.layout = QVBoxLayout(self)
        self.parent = parent
        self.child = None



    def disableTaps(self):
        self.centerWidget.tabs.setTabEnabled(1, False)
        self.centerWidget.tabs.setTabEnabled(4, False)
        self.centerWidget.tabs.setTabEnabled(5, False)

    def enableTaps(self):
        self.centerWidget.tabs.setTabEnabled(1, True)
        self.centerWidget.tabs.setTabEnabled(4, True)
        self.centerWidget.tabs.setTabEnabled(5, True)
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "<html><head/><body><p><img src=\":/backGround/1920X1030.png\"/></p></body></html>"))



class CenterWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        #  tap ini
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet('''QTabWidget::pane {
   border-top: 0px solid #C2C7CB;
    position: absolute;
    top: -0.1115em;
    
}
QTabWidget::tab-bar {
    alignment:center;
}
QTabBar::tab {
    background: transparent;
}''')
        """self.tabs.setStyleSheet('''QTabWidget::pane { /* The tab widget frame */
    border-top: 2px solid #C2C7CB;
}

QTabWidget::tab-bar {
    left: 5px; /* move to the right by 5px */
}

/* Style the tab using the tab sub-control. Note that
    it reads QTabBar _not_ QTabWidget */
QTabBar::tab {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,
                                stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);
    border: 2px solid #C4C4C3;
    border-bottom-color: #C2C7CB; /* same as the pane color */
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
    min-width: 8ex;
    padding: 2px;
}

QTabBar::tab:selected, QTabBar::tab:hover {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                stop: 0 #fafafa, stop: 0.4 #f4f4f4,
                                stop: 0.5 #e7e7e7, stop: 1.0 #fafafa);
}

QTabBar::tab:selected {
    border-color: #9B9B9B;
    border-bottom-color: #C2C7CB; /* same as pane color */
}

QTabBar::tab:!selected {
    margin-top: 2px; /* make non-selected tabs look smaller */
}''')"""
        self.tabs.currentChanged.connect(self.onChange)
        self.sell = sellPage.SellPage()
        self.logs = logs.Logs()
        self.Items = items.Items()
        self.users = users.Users()
        self.returns = returns.Returns()
        self.later = later.Later()
        self.logout = QWidget()
        # Taps management
        self.tabs.addTab(self.sell, '')
        self.tabs.addTab(self.logs, '')
        self.tabs.addTab(self.returns, '')
        self.tabs.addTab(self.later, '')
        self.tabs.addTab(self.Items, '')
        self.tabs.addTab(self.users, '')
        self.tabs.addTab(self.logout, '')
        # tap icons
        self.tabs.setTabIcon(0,QIcon('resources//shopping-cart@3x.png'))
        self.tabs.setTabIcon(1, QIcon('resources//sales.png'))
        self.tabs.setTabIcon(2, QIcon('resources//returns.png'))
        self.tabs.setTabIcon(3, QIcon('resources//agel@3x.png'))
        self.tabs.setTabIcon(4, QIcon('resources//list.png'))
        self.tabs.setTabIcon(5, QIcon('resources//users.png'))
        self.tabs.setTabIcon(6, QIcon('resources//sign-out.png'))


        self.tabs.setIconSize(items.QSize(137, 50))



        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)


    #  Taps Customization
    def onChange(self):
        # refreshTables
        self.Items.refreshTable()
        self.sell.refreshTable()
        self.logs.refreshAll()
        self.later.refreshTable()
