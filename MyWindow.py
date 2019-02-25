from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QTableWidgetItem
# from PyQt5.QtGui import QTextCursor,QTextCharFormat,QColor
from MainWindow import Ui_MainWindow

from Sematic import SematicAnalysis
from Mips import Assembler


# 语法高亮类
class Highlighter(QSyntaxHighlighter):
    def __init__(self, parent):
        QSyntaxHighlighter.__init__(self, parent)
        self.parent = parent
        self.highlightingRules = []

        # 数值类型
        format = QTextCharFormat()
        format.setForeground(Qt.darkGreen)
        format.setFontWeight(QFont.Bold)
        keywords = ["int", "void", "double"]
        for word in keywords:
            pattern = QRegExp('\\b' + word + '\\b')
            rule = {'pattern': pattern,
                    'format': format}
            self.highlightingRules.append(rule)

        # 关键字
        format_2 = QTextCharFormat()
        format_2.setForeground(Qt.blue)
        format_2.setFontWeight(QFont.Bold)
        # format_2.setFontItalic(True)
        keywords_2 = ["if", "else", "while", "return"]
        for word in keywords_2:
            pattern_2 = QRegExp('\\b' + word + '\\b')
            rule_2 = {'pattern': pattern_2,
                      'format': format_2}
            self.highlightingRules.append(rule_2)

        # 行号
        format_3 = QTextCharFormat()
        format_3.setForeground(Qt.red)
        pattern_3 = QRegExp(r'^[0-9]+\b')
        self.highlightingRules.append(
            {
                'pattern': pattern_3,
                'format': format_3
            })

    def highlightBlock(self, text):
        for rule in self.highlightingRules:
            expression = rule['pattern']
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, rule['format'])
                index = expression.indexIn(text, index + length)
        self.setCurrentBlockState(0)


class MyWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, syntax):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.syntax = syntax
        self.fname = ""
        self.synFinished = False
        self.semFinished = False
        self.setupUi(self)
        self.pushButton.clicked.connect(self.openFile)
        # self.pushButton_3.clicked.connect(self.saveFile)
        self.pushButton_2.clicked.connect(self.synAnalyze)
        self.pushButton_3.clicked.connect(self.semAnalyze)
        self.pushButton_4.clicked.connect(self.generateMIPS)
        self.textEdit_4.textChanged.connect(self.scrollToBottom)

        # 语法高亮
        highlighter = Highlighter(self.textEdit)

    def scrollToBottom(self):
        self.textEdit_4.moveCursor(QTextCursor.End)

    # 浏览文件对话框
    def openFile(self):
        self.fname, type = QFileDialog.getOpenFileName(self.centralwidget, "选择源代码", "./", "Text Files (*.txt)")
        self.textEdit_2.setText("")
        self.tableWidget.clearContents()
        self.tableWidget_2.clearContents()
        self.textEdit_3.setText("")
        if self.fname:
            f = open(self.fname, 'r')
            with f:
                self.synFinished = False
                self.semFinished = False
                text = f.read()
                self.textEdit.setText(self.showLineNumber(text))
                f.close()

    '''#保存文件对话框
    def saveFile(self):
        self.fname,type=QFileDialog.getSaveFileName(self.centralwidget,"保存源代码","./","Text Files (*.txt)")
        if self.fname:
            f=open(self.fname,'w')
            with f:
                f.write(self.textEdit.toPlainText())
                f.close()
    '''

    # 开始语法分析分析
    def synAnalyze(self):
        self.textEdit_2.setText("")
        self.tableWidget.clearContents()
        self.tableWidget_2.clearContents()
        self.textEdit_3.setText("")
        self.synFinished = False
        self.semFinished = False
        if self.fname:
            self.syntax.readFile(self.fname)
            self.textEdit.setText(self.showLineNumber(self.syntax.string))
            ErrorList, Procedure = self.syntax.analyze()
            Tree = self.syntax.getTree()
            self.textEdit_2.setText(Tree + '\n\n' + Procedure)
            text = self.textEdit_4.toPlainText()
            if self.syntax.ERROR == False:
                text += "语法分析完成, 0 error.\n\n"
                self.synFinished = True
            else:
                text += "语法分析完成, error(s)如下：\n" + ErrorList + "\n"
            self.textEdit_4.setText(text)
        else:
            QMessageBox.warning(self.centralwidget,
                                "警告", "请选择源代码文件",
                                QMessageBox.Yes)

    # 开始语义分析
    def semAnalyze(self):
        self.tableWidget.clearContents()
        self.tableWidget_2.clearContents()
        self.textEdit_3.setText("")
        self.semFinished = False
        if self.synFinished:
            if self.syntax.ERROR == False:
                self.synFinished = False
                treeHead = self.syntax.getTreeHead()
                self.sematic = SematicAnalysis(treeHead)
                symbolList, codeList, error = self.sematic.analyse()
                self.symbolList = symbolList
                self.codeList = codeList
                text = self.textEdit_4.toPlainText()
                if self.sematic.error == False:
                    text += "语义分析完成, 0 error.\n\n"
                    '''显示符号表'''
                    self.tableWidget.setRowCount(len(symbolList))
                    for i in range(len(symbolList)):
                        # 显示type
                        value = symbolList[i]['type']
                        item = QTableWidgetItem(value)
                        item.setTextAlignment(Qt.AlignCenter)
                        self.tableWidget.setItem(i, 0, item)
                        # 显示domain
                        value = symbolList[i]['domain']
                        item = QTableWidgetItem(value)
                        item.setTextAlignment(Qt.AlignCenter)
                        self.tableWidget.setItem(i, 1, item)
                        # 显示name
                        value = symbolList[i]['idName']
                        item = QTableWidgetItem(value)
                        item.setTextAlignment(Qt.AlignCenter)
                        self.tableWidget.setItem(i, 2, item)
                        # 显示label
                        value = symbolList[i]['label']
                        if value == 'data':
                            value = '变量'
                        elif value == 'func':
                            value = '函数'
                        elif value == 'formal':
                            value = '形参'
                        item = QTableWidgetItem(value)
                        item.setTextAlignment(Qt.AlignCenter)
                        self.tableWidget.setItem(i, 3, item)
                        # 显示offset
                        if symbolList[i]['label'] == 'data':
                            value = symbolList[i]['offset']
                            item = QTableWidgetItem(str(value))
                            item.setTextAlignment(Qt.AlignCenter)
                            self.tableWidget.setItem(i, 4, item)
                    '''显示四元式'''
                    self.tableWidget_2.setRowCount(len(codeList))
                    for i in range(len(codeList)):
                        # 显示addr
                        value = codeList[i]['addr']
                        item = QTableWidgetItem(str(value))
                        item.setTextAlignment(Qt.AlignCenter)
                        self.tableWidget_2.setItem(i, 0, item)
                        # 显示op
                        value = codeList[i]['op']
                        item = QTableWidgetItem(value)
                        item.setTextAlignment(Qt.AlignCenter)
                        self.tableWidget_2.setItem(i, 1, item)
                        # 显示arg1
                        if 'arg1' in codeList[i].keys():
                            value = codeList[i]['arg1']
                            if isinstance(value, dict):
                                if 'symbolIndex' in value.keys():
                                    index = value['symbolIndex']
                                    symbolItem = symbolList[index]
                                    value = symbolItem['idName'] + '_' + symbolItem['domain']
                                elif 'Imme' in value.keys():
                                    value = value['Imme']
                                elif 'reg' in value.keys():
                                    value = '$' + str(value['reg'])
                            item = QTableWidgetItem(str(value))
                            item.setTextAlignment(Qt.AlignCenter)
                            self.tableWidget_2.setItem(i, 2, item)
                        # 显示arg2
                        if 'arg2' in codeList[i].keys():
                            value = codeList[i]['arg2']
                            if isinstance(value, dict):
                                if 'symbolIndex' in value.keys():
                                    index = value['symbolIndex']
                                    symbolItem = symbolList[index]
                                    value = symbolItem['idName'] + '_' + symbolItem['domain']
                                elif 'Imme' in value.keys():
                                    value = value['Imme']
                                elif 'reg' in value.keys():
                                    value = '$' + str(value['reg'])
                            item = QTableWidgetItem(str(value))
                            item.setTextAlignment(Qt.AlignCenter)
                            self.tableWidget_2.setItem(i, 3, item)
                        # 显示result
                        if 'result' in codeList[i].keys():
                            value = codeList[i]['result']
                            if isinstance(value, dict):
                                if 'symbolIndex' in value.keys():
                                    index = value['symbolIndex']
                                    symbolItem = symbolList[index]
                                    value = symbolItem['idName'] + '_' + symbolItem['domain']
                                elif 'Imme' in value.keys():
                                    value = value['Imme']
                                elif 'reg' in value.keys():
                                    value = '$' + str(value['reg'])
                            item = QTableWidgetItem(str(value))
                            item.setTextAlignment(Qt.AlignCenter)
                            self.tableWidget_2.setItem(i, 4, item)
                    self.semFinished = True
                else:
                    text += "语义分析完成, error(s)如下：\n" + error + "\n"
                    '''QMessageBox.warning(self.centralwidget,
                                        "语义分析错误", "错误原因如下:\n" + error,
                                        QMessageBox.Yes)'''
                self.textEdit_4.setText(text)
            else:
                QMessageBox.warning(self.centralwidget,
                                    "警告", "语法分析错误\n无法进行语义分析",
                                    QMessageBox.Yes)
        else:
            QMessageBox.warning(self.centralwidget,
                                "警告", "请先完成语法分析",
                                QMessageBox.Yes)

    # 开始生成目标代码
    def generateMIPS(self):
        self.textEdit_3.setText("")
        if self.semFinished:
            if self.sematic.error == False:
                self.semFinished = False
                mipsGenerator = Assembler(self.symbolList, self.codeList)
                mips = mipsGenerator.generate()
                self.textEdit_3.setText(mips)
                text = self.textEdit_4.toPlainText()
                text += "生成目标代码成功.\n\n"
                self.textEdit_4.setText(text)
            else:
                text = self.textEdit_4.toPlainText()
                text += "语义分析错误，生成目标代码失败.\n\n"
                self.textEdit_4.setText(text)
                '''QMessageBox.warning(self.centralwidget,
                                    "警告", "语义分析错误\n无法产生目标代码",
                                    QMessageBox.Yes)'''
        else:
            QMessageBox.warning(self.centralwidget,
                                "警告", "请先完成语义分析",
                                QMessageBox.Yes)

    # 显示行号
    def showLineNumber(self, text):
        string = ""
        if text:
            linecnt = 1
            string += str(linecnt).ljust(4)
            i = 0
            while i < len(text):
                if text[i] == '\n':
                    linecnt += 1
                    string += '\n' + str(linecnt).ljust(4)
                    i += 1
                else:
                    string += text[i]
                    i += 1
            return string
