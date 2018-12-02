# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'homepage.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(437, 300)
        Dialog.setStyleSheet("background-color: rgb(142, 255, 180);")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(110, 10, 161, 31))
        self.label.setStyleSheet("font: 18pt \".SF NS Text\";")
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(53, 100, 161, 32))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(63, 180, 151, 32))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(Dialog)
        self.pushButton_3.setGeometry(QtCore.QRect(233, 180, 151, 32))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(Dialog)
        self.pushButton_4.setGeometry(QtCore.QRect(233, 100, 161, 32))
        self.pushButton_4.setObjectName("pushButton_4")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "           Homepage"))
        self.pushButton.setText(_translate("Dialog", "Currency Exchange"))
        self.pushButton_2.setText(_translate("Dialog", "London Exchange"))
        self.pushButton_3.setText(_translate("Dialog", "Shenzhen Exchange"))
        self.pushButton_4.setText(_translate("Dialog", "US Stock Exchange"))

