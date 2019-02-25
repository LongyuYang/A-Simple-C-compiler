from Production import Production, ProductionList
from Stack import MyStack
from lexicalAnalyze import LexAn
from Tree import node

'''LL1分析表类'''
class LL1Table():
    def __init__(self, Virables):
        self.table = {}
        for v in Virables:
            self.table[v] = {}

    def getPro(self, Virable, Terminal):
        return self.table[Virable][Terminal]

    def add(self, Virable, Terminal, Pro):
        self.table[Virable][Terminal] = Pro

'''语法分析器类'''
class SyntaxAnalysis:

    def __init__(self, InputPro):
        self.InputPro = InputPro
        self.Terminals = []
        self.TerAndEnd = []
        self.Virables = []
        self.start = ''
        self.pList = ProductionList()
        self.First = {}
        self.Follow = {}
        self.string = ''
        self.ERROR = False

    '''设置起始符号'''
    def setStart(self, s):
        self.start = s

    '''构造产生式表'''
    def buildProList(self):

        for p in self.InputPro:
            self.pList.add(Production(p[0], p[1]))
            if p[0] not in self.Virables:
                self.Virables.append(p[0])

        for p in self.InputPro:
            for t in p[1]:
                if t not in self.Virables and t not in self.Terminals and t != 'NULL':
                    self.Terminals.append(t)

        self.TerAndEnd = self.Terminals.copy()
        self.TerAndEnd.append('#')

    '''消除非终结符p的直接左递归'''
    def delDirectRecur(self, p):
        v = p
        vPList = self.pList.getVirablePro(v)
        isLeftRecur = False
        for p in vPList:
            if p.left == p.right[0]:
                isLeftRecur = True
        if isLeftRecur == True:
            new_v = v + '1'
            assert new_v not in self.Virables
            self.Virables.append(new_v)
            for p in vPList:
                if p.left == p.right[0]:
                    self.pList.delete(p)
                    p.right.remove(p.left)
                    p.right.append(new_v)
                    self.pList.add(Production(new_v, p.right))
                else:
                    if p.right == ['NULL']:
                        p.right = [new_v]
                    else:
                        p.right.append(new_v)
                    self.pList.add(Production(v, p.right))
            self.pList.add(Production(new_v, ['NULL']))

    '''消除左递归'''
    def delLeftRecur(self):
        for v in self.Virables:
            self.delDirectRecur(v)
        '''
        for i in range(0, len(self.Virables)):

            for j in range(0, i):
                piList = self.pList.getVirablePro(self.Virables[i])
                pjList = self.pList.getVirablePro(self.Virables[j])
                for pi in piList:
                    if pi.right[0] == self.Virables[j]:
                        self.pList.delete(pi)
                        for pj in pjList:
                            if pj.right == ['NULL']:
                                self.pList.add(Production(pi.left, pi.right[1:]))
                            else:
                                new = pj.right.copy()
                                new.extend(pi.right[1:])
                                self.pList.add(Production(pi.left, new))
            self.delDirectRecur(self.Virables[i])
        '''


    '''求FIRST集合'''
    def getFirst(self):
        first = {}
        for v in self.Virables:
            first[v] = []
        while (True):
            Modify = False
            for p in self.pList:
                if p.right[0] in self.Terminals:
                    if p.right[0] not in first[p.left]:
                        first[p.left].append(p.right[0])
                        Modify = True
                elif p.right == ['NULL']:
                    if 'NULL' not in first[p.left]:
                        first[p.left].append('NULL')
                        Modify = True
                else:
                    for i in range(len(p.right)):
                        if p.right[i] in self.Virables and i == 0:
                            for t in first[p.right[i]]:
                                if t not in first[p.left]:
                                    first[p.left].append(t)
                                    Modify = True
                        if p.right[i] in self.Virables and i >= 1 \
                            and p.right[i-1] in self.Virables \
                            and 'NULL' in first[p.right[i-1]]:
                            for t in first[p.right[i]]:
                                if t not in first[p.left]:
                                    first[p.left].append(t)
                                    Modify = True
                            if i == len(p.right) - 1 and \
                                'NULL' in first[p.right[i]]:
                                if 'NULL' not in first[p.left]:
                                    first[p.left].append('NULL')
                                    Modify = True

                        if p.right[i] in self.Terminals and i >= 1 \
                            and p.right[i - 1] in self.Virables \
                            and 'NULL' in first[p.right[i - 1]]:
                            if p.right[i] not in first[p.left]:
                                first[p.left].append(p.right[i])
                                Modify = True
                                break
            if not Modify:
                self.First = first
                break

    '''求FOLLOW集合'''
    def getFollow(self):

        follow = {}
        for v in self.Virables:
            follow[v] = []
            if v == self.start:
                follow[v].append('#')
        while (True):
            Modify = False
            for p in self.pList:
                i = len(p.right) - 1
                rightNull = True
                while (i >= 0):
                    if p.right[i] in self.Terminals:
                        rightNull = False
                    if p.right[i] in self.Virables:
                        if rightNull == True:
                            for t in follow[p.left]:
                                if t not in follow[p.right[i]]:
                                    follow[p.right[i]].append(t)
                                    Modify = True
                        if 'NULL' not in self.First[p.right[i]]:
                            rightNull = False
                        if i < len(p.right) - 1 and p.right[i+1] in self.Terminals:
                            if p.right[i+1] not in follow[p.right[i]]:
                                follow[p.right[i]].append(p.right[i+1])
                                Modify = True
                        if i < len(p.right) - 1 and p.right[i + 1] in self.Virables:
                            for t in self.First[p.right[i+1]]:
                                if t not in follow[p.right[i]] and t != 'NULL':
                                    follow[p.right[i]].append(t)
                                    Modify = True
                    i -= 1
            if not Modify:
                self.Follow = follow
                break

    '''求产生式的FIRST集合,之前须调用getFirst()'''
    def getProFirst(self, pro):
        first = []
        i = 0
        AllNull = True
        while (i < len(pro.right)):
            if pro.right[i] in self.Terminals:
                if pro.right[i] not in first:
                    first.append(pro.right[i])
                AllNull = False
                break
            elif pro.right[i] == 'NULL':
                break
            else:
                for t in self.First[pro.right[i]]:
                    if t not in first:
                        first.append(t)
                if 'NULL' not in self.First[pro.right[i]]:
                    AllNull = False
                    break
                else:
                    i += 1
        if AllNull:
            first.append('NULL')
        return first

    '''判断是否为LL1文法'''
    def isLL1(self):
        for v in self.Virables:
            pro = self.pList.getVirablePro(v)
            for p in pro:
                for q in pro:
                    if p != q:
                        first_p = self.getProFirst(p)
                        first_q = self.getProFirst(q)
                        for t in first_p:
                            if t in first_q:
                                print (p.right,q.right)
                                return False
            if 'NULL' in self.First[v]:
                for t in self.First[v]:
                    if t in self.Follow[v]:
                        print (self.First[v])
                        print (self.Follow[v])
                        print (v)
                        return False
        return True

    '''构造LL1分析表'''
    def buildLL1Table(self):
        self.Table = LL1Table(self.Virables)
        for p in self.pList:
            first_p = self.getProFirst(p)
            for t in first_p:
                self.Table.add(p.left, t, p)
            if 'NULL' in first_p:
                for k in self.Follow[p.left]:
                    self.Table.add(p.left, k, p)

        for v in self.Virables:
            for t in self.TerAndEnd:
                if t not in self.Table.table[v]:
                    if t in self.Follow[v]:
                        self.Table.table[v][t] = 'synch'
                    else:
                        self.Table.table[v][t] = ' '

    def showLL1Table(self):
        for v in self.Virables:
            for t in self.TerAndEnd:
                if self.Table.table[v][t] == ' ' or self.Table.table[v][t] == 'synch':
                    print (v, t, self.Table.table[v][t])
                else:
                    print (v, t, self.Table.table[v][t].left, self.Table.table[v][t].right)

    '''读取待分析文件'''
    def readFile(self, fileName):
        f = open(fileName, 'r')
        self.string = f.read()
        f.close()

    '''读取待分析字符串'''
    def getString(self, s):
        self.string = s

    '''读取下一个词'''
    def advance(self):
        while (self.pointer < len(self.string)):
            if self.string[self.pointer] in ['\n', '\t', ' ']:
                if self.string[self.pointer] == '\n':
                    self.lineCounter += 1
                self.pointer += 1
            else:
                end, label = self.lex.lex_analyze(self.pointer)
                word = self.string[self.pointer:end+1]
                self.pointer = end + 1
                if label == '标识符':
                    now = '标识符'
                elif label == '数值':
                    now = 'num'
                else:
                    now = word
                return word, label, now
        return -1, -1, -1  #越界

    '''语法分析'''
    def analyze(self):
        self.ERROR = False
        self.head = node()
        self.head.setData('head')

        stack = MyStack()
        self.lex = LexAn(self.string)

        endNode = node()
        endNode.setData('#')
        stack.push(endNode)

        startNode = node()
        startNode.setData(self.start)
        startNode.setParent(self.head)
        self.head.addChildren(startNode)
        stack.push(startNode)

        self.pointer = 0
        self.lineCounter = 1
        word, label, now = self.advance()
        outResult = ''
        ErrorResult = ''
        while (True):
            '''遇注释号跳过'''
            if label == '注释号':
                word, label, now = self.advance()
                continue

            '''文件读完,未完成语法分析'''
            if word == -1:
                ErrorResult += ('line %d:' % self.lineCounter + ' 语法分析错误结束\n')
                outResult += '\n'
                break

            '''遇非法字符'''
            if label == 'ERROR':
                ErrorResult += ('line %d:' % self.lineCounter + ' 跳过非法词%s\n'%word)
                outResult += '\n'
                word, label, now = self.advance()
                continue

            out = ('line %d: '%self.lineCounter
                        + word +','+ label)
            outResult = outResult + out.ljust(20, ' ')

            proResult = False
            topNode = stack.pop()
            X = topNode.data

            if X in self.Terminals:
                if X == now:
                    if X == "标识符":
                        topNode.addAttributes("idName", word)
                    if X == "num":
                        topNode.addAttributes("NumValue", word)
                    topNode.addAttributes("lineNum", self.lineCounter)
                    word, label, now = self.advance()
                else:
                    ErrorResult += ('line %d:'%self.lineCounter + ' 期待%s\n'%(X))
                    outResult += '\n'
                    continue
            elif X == '#':
                if X == now:
                    break
                else:
                    ErrorResult += ('line %d:'%self.lineCounter + ' 检查%s附近\n'%(word))
                    outResult += '\n'
                    break
            elif X in self.Virables and self.Table.table[X][now] not in [' ', 'synch']:
                if self.Table.table[X][now].right == ['NULL']:
                    newNode = node()
                    newNode.setParent(topNode)
                    newNode.setData('NULL')
                    topNode.addChildren(newNode)
                    pass
                else:
                    k = len(self.Table.table[X][now].right) - 1
                    while (k >= 0):
                        newNode = node()
                        newNode.setParent(topNode)
                        newNode.setData(self.Table.table[X][now].right[k])
                        topNode.addChildren(newNode)
                        stack.push(newNode)
                        k -= 1
                    topNode.reverseChildren()
                out = ('产生式: ' + self.Table.table[X][now].left
                              +'-->'+' '.join(self.Table.table[X][now].right))
                outResult += out.ljust(40, ' ')

                proResult = True
            else:
                if len(stack.s) == 1 or self.Table.table[X][now] == ' ':
                    newNode = node()
                    newNode.setData(X)
                    stack.push(newNode)
                    ErrorResult += ('line %d:'%self.lineCounter + ' 跳过%s, 检查%s附近\n'%(word, word))
                    word, label, now = self.advance()
                    if word == -1:
                        ErrorResult += ('line %d:' % self.lineCounter + ' 语法分析错误结束\n')
                        outResult += '\n'
                        break
                elif self.Table.table[X][now] == 'synch':
                    ErrorResult += ('line %d:'%self.lineCounter + ' %s出栈, 检查%s附近\n'%(X, word))
                outResult += '\n'
                continue
            if not proResult:
                outResult += ' '.ljust(40)

            outResult += (('栈: ' + stack.show()).ljust(40)+'\n')

        if ErrorResult == '':
            return ErrorResult, outResult
        else:
            self.ERROR = True
            return ErrorResult, outResult

    '''获取语法分析树'''
    def getTree(self):
        if self.ERROR:
            return "出现错误, 不显示语法分析树"
        self.lines = []
        self.recurrentGetTree(self.head, 0)
        return '\n'.join(self.lines)

    def recurrentGetTree(self, p, layer):
        if layer >= 1:
            line = '  ' * (layer-1) +'|_'+ p.data
            if p.data == "标识符":
                line += (": "+p.attributes["idName"])
            if p.data == "num":
                line += (": " + p.attributes["NumValue"])
            self.lines.append(line)
            i = len(self.lines)-2
            pointer = 2*(layer-1)
            while (True):
                if (self.lines[i][pointer]) != ' ':
                    break
                str_list = list(self.lines[i])
                str_list[pointer] = '|'
                self.lines[i] = ''.join(str_list)
                i -= 1
        if len(p.children) == 0:
            return
        for c in p.children:
            self.recurrentGetTree(c, layer+1)

    def getTreeHead(self):
        return self.head







