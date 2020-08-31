from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.uic.properties import QtWidgets
from passlib.hash import pbkdf2_sha256

import popups
import DB
import CommonFunctions
import MyConstants

global userName
userName = None


class Users(QMainWindow):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        uic.loadUi('users.ui', self)
        #  VARS   Initialization
        self.addUserName = None
        self.addUserPassword = None
        self.addUserPasswordRepeat = None
        self.addUserAdmin = None
        self.editUserName = None
        self.editUserPassword = None
        self.editUserPasswordRepeat = None
        self.editUserAdmin = None
        self.editNewUserName = None
        self.userColumns = MyConstants.userColumns
        #  Page initialization
        self.tableWidget.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tableWidget.itemSelectionChanged.connect(self.selectionChanged)

        # Button Clicked
        self.pushButton_addUser.clicked.connect(self.addUser)
        self.pushButton_edit.clicked.connect(self.editUser)
        self.pushButton_reomveUser.clicked.connect(self.removeUser)
        self.refreshTable()

    def addUser(self):
        self.getInput()
        if CommonFunctions.checkIfVailed(self.addUserName, self.addUserPassword, self.addUserPasswordRepeat):
            if CommonFunctions.isNew(self.addUserName):
                if CommonFunctions.validate(self.addUserPassword):
                    if self.checkBox.isChecked():
                        self.addUserAdmin = 1
                    else:
                        self.addUserAdmin = 0
                    DB.dB.insertInto((self.addUserName, pbkdf2_sha256.hash(self.addUserPassword), self.addUserAdmin),
                                     MyConstants.insertUsers)
                    popups.showMessage("تم", "تم ادخال مستخدم جديد")
                    self.clearALl()
                    self.refreshTable()
                else:
                    self.clearALl(AddUser=False)
            else:
                popups.showMessage("خطا", "هذا المستخدم موجود سابقا")
                self.clearALl(AddUser=False)
        else:
            self.clearALl(AddUser=False)

    def editUser(self):
        flag = False
        self.getInput()
        result = DB.dB.selectByName('users', self.editUserName)
        defaultUserName = result[0][1]
        defaultAdmin = result[0][3]
        self.editUserAdmin = CommonFunctions.updateSelector(str(self.editUserAdmin), str(defaultAdmin))
        if not CommonFunctions.isEmpty(self.editNewUserName):
            if not self.isDub():
                self.editNewUserName = self.editNewUserName
        else:
            self.editNewUserName = defaultUserName
        if not CommonFunctions.isEmpty(self.editUserPassword):
            if CommonFunctions.validate(self.editUserPassword):
                if self.editUserPassword == self.editUserPasswordRepeat:
                    flag = True
                else:
                    popups.showMessage('خطأ', 'كلمة المرور غير متطابقة')
                    self.clearALl()
                    return True
        if flag:
            user = (self.editNewUserName, pbkdf2_sha256.hash(self.editUserPassword), self.editUserAdmin,
                    int(result[0][0]))
            DB.dB.updateTo(user, MyConstants.updateUsers)
        else:
            user = (self.editNewUserName, self.editUserAdmin, int(result[0][0]))
            DB.dB.updateTo(user, MyConstants.updateUsersWithoutPasswordChange)
        popups.showMessage("تم", "تم تعديل المستخدم ")
        self.clearALl()
        self.refreshTable()

    def refreshTable(self):
        self.tableWidget.clearSelection()
        self.tableWidget.setRowCount(0);
        users = DB.dB.selectSpecificColumnsFromTable(self.userColumns, 'users')
        for row_number, user in enumerate(users):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(user):
                cell = QTableWidgetItem(str(data))
                self.tableWidget.setItem(row_number, column_number, cell)

    def getInput(self):
        try:
            self.addUserName = self.lineEdit_user.text()
            self.addUserPassword = self.lineEdit_password.text()
            self.addUserPasswordRepeat = self.lineEdit_passwordRepeat.text()
            self.editNewUserName = self.lineEdit_user_2.text()
            self.editUserPassword = self.lineEdit_password_2.text()
            self.editUserPasswordRepeat = self.lineEdit_passwordRepeat_2.text()
            if self.checkBox_2.isChecked():
                self.editUserAdmin = 1
            else:
                self.editUserAdmin = 0
        except Exception as e:
            print(e)

    def selectionChanged(self):
        self.editUserName = self.tableWidget.item(self.getSelectedRow(), 0).text()

    def getSelectedRow(self):
        return self.tableWidget.currentRow()

    def isDub(self):
        result = DB.dB.selectByName('users', self.editNewUserName)
        if len(result) == 1:
            return True
        else:
            return False

    def removeUser(self):
        admins = 0
        users = DB.dB.selectAllFrom('users')
        for user in users:
            if user[3] == 1:
                admins += 1
        thisUser = DB.dB.selectByName('users', self.editUserName)
        if admins > 1 or thisUser[0][3] == 0:
            dialog = popups.Confirmation(self, 'ان تمسح هذا المستخدم :')
            dialog.show()
            res = dialog.exec_()
            if res == dialog.Accepted:
                try:
                    DB.dB.deleteByNameFrom('users', self.editUserName)
                    self.refreshTable()
                    self.clearALl()
                except:
                    pass
            else:
                pass
        else:
            popups.showMessage("خطا", "لايمكنك ازاله اخر ادمن فى النظام")

    def clearALl(self, AddUser=True, EditUser=True):
        if AddUser:
            self.lineEdit_user.clear()
            self.checkBox.setCheckState(False)
        self.lineEdit_password.clear()
        self.lineEdit_passwordRepeat.clear()
        if EditUser:
            self.lineEdit_user_2.clear()
            self.checkBox_2.setCheckState(False)
        self.lineEdit_password_2.clear()
        self.lineEdit_passwordRepeat_2.clear()


class User:
    def __init__(self):
        self.userName = None

    def setUserName(self, user):
        global userName
        userName = user

    def returnUserName(self):
        return userName
