# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'EntryForm.ui'
#
# Created: Tue Nov 18 19:31:21 2014
#      by: pyside-uic 0.2.13 running on PySide 1.1.0
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(624, 411)
        self.centralWidget = QtGui.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.fn = QtGui.QLineEdit(self.centralWidget)
        self.fn.setGeometry(QtCore.QRect(100, 40, 201, 31))
        self.fn.setObjectName("fn")
        self.label = QtGui.QLabel(self.centralWidget)
        self.label.setGeometry(QtCore.QRect(10, 40, 81, 31))
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.ln = QtGui.QLineEdit(self.centralWidget)
        self.ln.setGeometry(QtCore.QRect(390, 40, 161, 31))
        self.ln.setObjectName("ln")
        self.label_2 = QtGui.QLabel(self.centralWidget)
        self.label_2.setGeometry(QtCore.QRect(310, 40, 81, 31))
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.ad = QtGui.QLineEdit(self.centralWidget)
        self.ad.setGeometry(QtCore.QRect(100, 90, 451, 31))
        self.ad.setObjectName("ad")
        self.label_3 = QtGui.QLabel(self.centralWidget)
        self.label_3.setGeometry(QtCore.QRect(10, 90, 81, 31))
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.st = QtGui.QLineEdit(self.centralWidget)
        self.st.setGeometry(QtCore.QRect(390, 140, 41, 31))
        self.st.setObjectName("st")
        self.ct = QtGui.QLineEdit(self.centralWidget)
        self.ct.setGeometry(QtCore.QRect(100, 140, 201, 31))
        self.ct.setObjectName("ct")
        self.label_4 = QtGui.QLabel(self.centralWidget)
        self.label_4.setGeometry(QtCore.QRect(10, 140, 81, 31))
        self.label_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtGui.QLabel(self.centralWidget)
        self.label_5.setGeometry(QtCore.QRect(300, 140, 81, 31))
        self.label_5.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName("label_5")
        self.label_6 = QtGui.QLabel(self.centralWidget)
        self.label_6.setGeometry(QtCore.QRect(430, 140, 81, 31))
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.zp = QtGui.QLineEdit(self.centralWidget)
        self.zp.setGeometry(QtCore.QRect(490, 140, 61, 31))
        self.zp.setObjectName("zp")
        self.em = QtGui.QLineEdit(self.centralWidget)
        self.em.setGeometry(QtCore.QRect(100, 190, 451, 31))
        self.em.setObjectName("em")
        self.label_7 = QtGui.QLabel(self.centralWidget)
        self.label_7.setGeometry(QtCore.QRect(10, 190, 81, 31))
        self.label_7.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_7.setObjectName("label_7")
        self.pbc = QtGui.QPushButton(self.centralWidget)
        self.pbc.setGeometry(QtCore.QRect(100, 300, 91, 27))
        self.pbc.setObjectName("pbc")
        self.pbs = QtGui.QPushButton(self.centralWidget)
        self.pbs.setGeometry(QtCore.QRect(280, 300, 91, 27))
        self.pbs.setObjectName("pbs")
        self.pbl = QtGui.QPushButton(self.centralWidget)
        self.pbl.setGeometry(QtCore.QRect(460, 300, 91, 27))
        self.pbl.setObjectName("pbl")
        self.errorLabel = QtGui.QLabel(self.centralWidget)
        self.errorLabel.setGeometry(QtCore.QRect(100, 240, 451, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setWeight(75)
        font.setBold(True)
        self.errorLabel.setFont(font)
        self.errorLabel.setText("")
        self.errorLabel.setObjectName("errorLabel")
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtGui.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 624, 25))
        self.menuBar.setObjectName("menuBar")
        MainWindow.setMenuBar(self.menuBar)
        self.mainToolBar = QtGui.QToolBar(MainWindow)
        self.mainToolBar.setObjectName("mainToolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtGui.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.fn, self.ln)
        MainWindow.setTabOrder(self.ln, self.ad)
        MainWindow.setTabOrder(self.ad, self.ct)
        MainWindow.setTabOrder(self.ct, self.st)
        MainWindow.setTabOrder(self.st, self.zp)
        MainWindow.setTabOrder(self.zp, self.em)
        MainWindow.setTabOrder(self.em, self.pbc)
        MainWindow.setTabOrder(self.pbc, self.pbs)
        MainWindow.setTabOrder(self.pbs, self.pbl)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "First Name", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MainWindow", "Last Name", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("MainWindow", "Address", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("MainWindow", "City", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("MainWindow", "State", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("MainWindow", "ZIP", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("MainWindow", "Email", None, QtGui.QApplication.UnicodeUTF8))
        self.pbc.setText(QtGui.QApplication.translate("MainWindow", "Clear", None, QtGui.QApplication.UnicodeUTF8))
        self.pbs.setText(QtGui.QApplication.translate("MainWindow", "Save...", None, QtGui.QApplication.UnicodeUTF8))
        self.pbl.setText(QtGui.QApplication.translate("MainWindow", "Load...", None, QtGui.QApplication.UnicodeUTF8))

