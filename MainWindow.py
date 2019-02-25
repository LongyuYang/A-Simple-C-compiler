# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1501, 921)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(11, 11, 331, 661))
        self.groupBox.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.textEdit = QtWidgets.QTextEdit(self.groupBox)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        self.textEdit.setFont(font)
        self.textEdit.setStyleSheet("")
        self.textEdit.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.textEdit.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.textEdit.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
        self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName("textEdit")
        self.gridLayout_2.addWidget(self.textEdit, 0, 0, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.groupBox)
        self.pushButton.setMinimumSize(QtCore.QSize(100, 0))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(10)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("QPushButton{\n"
"background-color:rgba(225,225,225,180);\n"
"border-style:outset;\n"
"border-width:2px;\n"
"border-color:rgba(0,0,0,30);\n"
"color:rgba(0,0,0,200);\n"
"padding:6px;}\n"
"QPushButton:pressed{\n"
"background-color:rgba(205,230,255,200);\n"
"border-color:rgba(0,120,215,30);\n"
"border-style:inset;\n"
"color:rgba(0,0,0,100);}\n"
"QPushButton:hover{\n"
"background-color:rgba(230,240,250,100);\n"
"border-color:rgba(0,120,215,200);\n"
"color:rgba(0,0,0,200);}\n"
"")
        self.pushButton.setObjectName("pushButton")
        self.gridLayout_2.addWidget(self.pushButton, 1, 0, 1, 1, QtCore.Qt.AlignRight)
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(340, 11, 331, 661))
        self.groupBox_2.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.textEdit_2 = QtWidgets.QTextEdit(self.groupBox_2)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        self.textEdit_2.setFont(font)
        self.textEdit_2.setStyleSheet("")
        self.textEdit_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.textEdit_2.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.textEdit_2.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
        self.textEdit_2.setReadOnly(True)
        self.textEdit_2.setObjectName("textEdit_2")
        self.gridLayout_3.addWidget(self.textEdit_2, 0, 0, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton_2.setMinimumSize(QtCore.QSize(100, 0))
        font = QtGui.QFont()
        font.setFamily("宋体")
        self.pushButton_2.setFont(font)
        self.pushButton_2.setStyleSheet("QPushButton{\n"
"background-color:rgba(225,225,225,180);\n"
"border-style:outset;\n"
"border-width:2px;\n"
"border-color:rgba(0,0,0,30);\n"
"color:rgba(0,0,0,200);\n"
"padding:6px;}\n"
"QPushButton:pressed{\n"
"background-color:rgba(205,230,255,200);\n"
"border-color:rgba(0,120,215,30);\n"
"border-style:inset;\n"
"color:rgba(0,0,0,100);}\n"
"QPushButton:hover{\n"
"background-color:rgba(230,240,250,100);\n"
"border-color:rgba(0,120,215,200);\n"
"color:rgba(0,0,0,200);}\n"
"")
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout_3.addWidget(self.pushButton_2, 1, 0, 1, 1, QtCore.Qt.AlignRight)
        self.groupBox_3 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_3.setGeometry(QtCore.QRect(670, 11, 481, 661))
        self.groupBox_3.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.groupBox_3.setFont(font)
        self.groupBox_3.setObjectName("groupBox_3")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox_3)
        self.gridLayout.setObjectName("gridLayout")
        self.tableWidget = QtWidgets.QTableWidget(self.groupBox_3)
        self.tableWidget.setStyleSheet("")
        self.tableWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.tableWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setObjectName("tableWidget")
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(87)
        self.tableWidget.verticalHeader().setVisible(False)
        self.gridLayout.addWidget(self.tableWidget, 0, 0, 1, 1)
        self.tableWidget_2 = QtWidgets.QTableWidget(self.groupBox_3)
        self.tableWidget_2.setStyleSheet("")
        self.tableWidget_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.tableWidget_2.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget_2.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget_2.setObjectName("tableWidget_2")
        self.tableWidget_2.setColumnCount(5)
        self.tableWidget_2.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(4, item)
        self.tableWidget_2.horizontalHeader().setVisible(True)
        self.tableWidget_2.horizontalHeader().setDefaultSectionSize(87)
        self.tableWidget_2.verticalHeader().setVisible(False)
        self.gridLayout.addWidget(self.tableWidget_2, 1, 0, 1, 1)
        self.pushButton_3 = QtWidgets.QPushButton(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_3.sizePolicy().hasHeightForWidth())
        self.pushButton_3.setSizePolicy(sizePolicy)
        self.pushButton_3.setMinimumSize(QtCore.QSize(100, 0))
        font = QtGui.QFont()
        font.setFamily("宋体")
        self.pushButton_3.setFont(font)
        self.pushButton_3.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.pushButton_3.setStyleSheet("QPushButton{\n"
"background-color:rgba(225,225,225,180);\n"
"border-style:outset;\n"
"border-width:2px;\n"
"border-color:rgba(0,0,0,30);\n"
"color:rgba(0,0,0,200);\n"
"padding:6px;}\n"
"QPushButton:pressed{\n"
"background-color:rgba(205,230,255,200);\n"
"border-color:rgba(0,120,215,30);\n"
"border-style:inset;\n"
"color:rgba(0,0,0,100);}\n"
"QPushButton:hover{\n"
"background-color:rgba(230,240,250,100);\n"
"border-color:rgba(0,120,215,200);\n"
"color:rgba(0,0,0,200);}\n"
"")
        self.pushButton_3.setObjectName("pushButton_3")
        self.gridLayout.addWidget(self.pushButton_3, 2, 0, 1, 1)
        self.groupBox_4 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_4.setGeometry(QtCore.QRect(1150, 11, 341, 661))
        self.groupBox_4.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.groupBox_4.setFont(font)
        self.groupBox_4.setObjectName("groupBox_4")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.groupBox_4)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.textEdit_3 = QtWidgets.QTextEdit(self.groupBox_4)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        self.textEdit_3.setFont(font)
        self.textEdit_3.setStyleSheet("")
        self.textEdit_3.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.textEdit_3.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.textEdit_3.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
        self.textEdit_3.setReadOnly(True)
        self.textEdit_3.setObjectName("textEdit_3")
        self.gridLayout_5.addWidget(self.textEdit_3, 0, 0, 1, 1)
        self.pushButton_4 = QtWidgets.QPushButton(self.groupBox_4)
        self.pushButton_4.setMinimumSize(QtCore.QSize(100, 0))
        font = QtGui.QFont()
        font.setFamily("宋体")
        self.pushButton_4.setFont(font)
        self.pushButton_4.setStyleSheet("QPushButton{\n"
"background-color:rgba(225,225,225,180);\n"
"border-style:outset;\n"
"border-width:2px;\n"
"border-color:rgba(0,0,0,30);\n"
"color:rgba(0,0,0,200);\n"
"padding:6px;}\n"
"QPushButton:pressed{\n"
"background-color:rgba(205,230,255,200);\n"
"border-color:rgba(0,120,215,30);\n"
"border-style:inset;\n"
"color:rgba(0,0,0,100);}\n"
"QPushButton:hover{\n"
"background-color:rgba(230,240,250,100);\n"
"border-color:rgba(0,120,215,200);\n"
"color:rgba(0,0,0,200);}\n"
"")
        self.pushButton_4.setObjectName("pushButton_4")
        self.gridLayout_5.addWidget(self.pushButton_4, 1, 0, 1, 1, QtCore.Qt.AlignRight)
        self.groupBox_5 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_5.setGeometry(QtCore.QRect(10, 670, 1481, 241))
        self.groupBox_5.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.groupBox_5.setFont(font)
        self.groupBox_5.setObjectName("groupBox_5")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.groupBox_5)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.textEdit_4 = QtWidgets.QTextEdit(self.groupBox_5)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        self.textEdit_4.setFont(font)
        self.textEdit_4.setStyleSheet("")
        self.textEdit_4.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.textEdit_4.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.textEdit_4.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
        self.textEdit_4.setReadOnly(True)
        self.textEdit_4.setObjectName("textEdit_4")
        self.gridLayout_4.addWidget(self.textEdit_4, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "编译器"))
        self.groupBox.setTitle(_translate("MainWindow", "源程序"))
        self.pushButton.setText(_translate("MainWindow", "浏览"))
        self.groupBox_2.setTitle(_translate("MainWindow", "词法与语法分析"))
        self.pushButton_2.setText(_translate("MainWindow", "分析"))
        self.groupBox_3.setTitle(_translate("MainWindow", "语义分析与中间代码"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "type"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "domain"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "name"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "label"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "offset"))
        item = self.tableWidget_2.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "addr"))
        item = self.tableWidget_2.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "op"))
        item = self.tableWidget_2.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "arg1"))
        item = self.tableWidget_2.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "arg2"))
        item = self.tableWidget_2.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "result"))
        self.pushButton_3.setText(_translate("MainWindow", "生成"))
        self.groupBox_4.setTitle(_translate("MainWindow", "目标代码"))
        self.pushButton_4.setText(_translate("MainWindow", "产生"))
        self.groupBox_5.setTitle(_translate("MainWindow", "错误信息"))

