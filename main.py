from Syntax import SyntaxAnalysis
from Sematic import SematicAnalysis
from Mips import Assembler
from Production import getCPro

import sys
from PyQt5.QtWidgets import QApplication
from MyWindow import MyWindow

if __name__ == '__main__':


    inputPro = getCPro()               #获取产生式
    syntax = SyntaxAnalysis(inputPro)  #构造语法分析器
    syntax.buildProList()              #构造产生式表
    syntax.setStart('Program')         #设置起始符号
    syntax.delLeftRecur()              #消除左递归
    syntax.getFirst()                  #求FIRST集合
    syntax.getFollow()                 #求FOLLOW集合
    #syntax.isLL1()                    #判断是否LL1
    syntax.buildLL1Table()             #构造LL1分析表
    #syntax.showLL1Table()             #展示LL1分析表
    '''syntax.readFile('test.txt')        #读取待分析文件
    ERRORresult, STACKresult = syntax.analyze()   #语法分析,返回要错误信息和栈信息
    tree = syntax.getTree()            #获取语法分析树
    #print (tree)
    f = open('result.txt', 'w')
    f.write(ERRORresult + '\n' + STACKresult)
    f.close()
    if syntax.ERROR == False:
        treeHead = syntax.getTreeHead()                      #获取语法分析树树根
        sematic = SematicAnalysis(treeHead)                  #创建语义分析器
        symbolList, codeList, error = sematic.analyse()      #语义分析
        print(symbolList)
        print(codeList)
        if sematic.error == False:
            mipsGenerator = Assembler(symbolList, codeList)  #创建汇编生成器
            mips = mipsGenerator.generate()                  #生成汇编代码
            #print (mips)
        else:
            print (error)'''

    a = QApplication(sys.argv)
    w = MyWindow(syntax)
    w.show()
    sys.exit(a.exec_())









