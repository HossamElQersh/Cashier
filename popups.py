from PyQt5.QtWidgets import *
from PyQt5 import uic


class Confirmation(QDialog):
    def __init__(self, parent, text):
        QDialog.__init__(self, parent)
        uic.loadUi('resources//confirmation.ui', self)
        self.label_toChange.setText(text)


class MoreItems(QDialog):
    def __init__(self, parent, maxValue):
        QDialog.__init__(self, parent)
        uic.loadUi('resources//quantity.ui', self)
        self.maxValue = maxValue
        self.lineEdit_Quantity_2.textChanged.connect(self.textChanged)
        self.horizontalSlider.setMinimum(1)
        self.horizontalSlider.setMaximum(self.maxValue)
        self.horizontalSlider.valueChanged.connect(self.valuechange)

    def valuechange(self):
        self.lineEdit_Quantity_2.setText(str(self.horizontalSlider.value()))

    def textChanged(self):
        try:
            value = int(self.lineEdit_Quantity_2.text())
            if self.maxValue < value:
                showMessage('خطا', 'لايمكن اضافة رقم اكبر من القيمة المتاحة')
                self.lineEdit_Quantity_2.setText(str('1'))
            try:
                self.horizontalSlider.setValue(int(self.lineEdit_Quantity_2.text()))
            except Exception as e:
                print(e)
        except:
            self.lineEdit_Quantity_2.clear()


class Refill(QDialog):
    def __init__(self, parent):
        QDialog.__init__(self, parent)
        uic.loadUi('resources//refill.ui', self)


class Later(QDialog):
    def __init__(self, parent,totalPrice):
        QDialog.__init__(self, parent)
        uic.loadUi('resources//laterForm.ui', self)
        self.lineEdit_Payed.editingFinished.connect(self.checkingPayed)
        self.lineEdit_Amount.setText("{:,.2f} EGP".format(totalPrice))
        self.name = None
        self.amount = totalPrice
        self.payed = 0

    def checkingPayed(self):
        try:
            self.payed = self.lineEdit_Payed.text()
            self.payed = float(self.payed)
        except:
            self.payed = 0
            self.lineEdit_Payed.setText(str(self.payed))


def showMessage(title="Error", message="Error"):
    QMessageBox.information(None, title, message)
