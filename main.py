import sys

import qdarkgraystyle
from PyQt5 import QtCore, QtNetwork, QtWidgets, uic, Qt
import MainWindow
import DB
import CommonFunctions
import users
import MyConstants
import resourceFiles_rc
global userName
userName = None


class UniqueApplication(QtWidgets.QApplication):
    anotherInstance = QtCore.pyqtSignal()

    def isUnique(self):
        socket = QtNetwork.QLocalSocket()
        socket.connectToServer('myApp')
        return not socket.state()

    def startListener(self):
        self.listener = QtNetwork.QLocalServer(self)
        self.listener.setSocketOptions(self.listener.WorldAccessOption)
        self.listener.newConnection.connect(self.anotherInstance)
        self.listener.listen('myApp')
        print('waiting for connections on "{}"'.format(self.listener.serverName()))


def showUI(admin):
    if admin == 1:
        app_window.show()
        app_window.setFixedSize(1920,1010)
        app_window.centerWidget.tabs.setCurrentIndex(0)
        app_window.enableTaps()
    else:
        app_window.show()
        app_window.setFixedSize(1920, 1010)
        app_window.centerWidget.tabs.setCurrentIndex(0)
        app_window.disableTaps()


def logout(index):
    if index == 6:
        login_window.show()
        app_window.hide()


def login():
    user = login_window.lineEdit_user.text()
    password = login_window.lineEdit_password.text()
    result = DB.dB.selectByName('users', user)
    if CommonFunctions.checkPassword(user, password, result):
        login_window.lineEdit_password.clear()
        login_window.lineEdit_user.clear()
        users.User.setUserName(users.User, user)
        showUI(result[0][3])
        login_window.hide()

    else:
        login_window.lineEdit_password.clear()


if __name__ == '__main__':
    app = UniqueApplication(sys.argv)
    if not app.isUnique():
        print('Application already running!')
    else:
        app.startListener()

        login_window = uic.loadUi('resources\\test.ui')
        login_window.setWindowFlags(MyConstants.dialogFlags)
        User = login_window.pushButton_login.clicked.connect(login)
        login_window.show()
        app_window = MainWindow.MainWindow()
        app_window.setWindowFlags(MyConstants.mainWindowFlags)
        app_window.centerWidget.tabs.tabBarClicked.connect(logout)
        app_window.hide()
        sys.exit(app.exec_())
