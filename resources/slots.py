from PyQt5 import QtCore, QtNetwork, QtWidgets, uic, Qt
import sys

from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':
    app = QApplication([])
    login_window = uic.loadUi('login.ui')

    login_window.show()
    sys.exit(app.exec_())