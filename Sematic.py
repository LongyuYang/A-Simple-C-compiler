from Tree import node
from Stack import MyStack

class SematicAnalysis():
    def __init__(self, head):
        self.symbolList = []
        self.codeList = []
        self.treeHead = head
        self.offset = 0
        self.domain = "global"
        self.error = False
        self.errorReason = []
        self.regCount = 7
        self.codeStack = MyStack()
        self.paramStack = MyStack()
        self.funCode = {}
        self.haveReturn = True

    def newReg(self):
        if self.regCount == 24:
            self.regCount = 7
        self.regCount += 1
        return self.regCount

    def lookUpSymbol(self, name, domain):

        for i in range(len(self.symbolList)):
            if self.symbolList[i]["idName"] == name and self.symbolList[i]["domain"] == domain:
                return i, self.symbolList[i]["domain"]
        for i in range(len(self.symbolList)):
            if self.symbolList[i]["idName"] == name:
                return i, self.symbolList[i]["domain"]
        return -1, "NULL"

    def arrangeAddr(self):
        codeList = []
        unknownList = []
        funAddr = {}
        counter = 0
        funAddr['main'] = 100
        self.funCode['main'][-1]['result'] = 'end'
        for c in self.funCode['main']:
            c['addr'] = 100 + counter
            if c['op'][0] == 'j':
                try:
                    if c['result'][:3] == 'to_':
                        c['result'] = c['result'][3:]
                        unknownList.append(counter)
                except:
                    c['result'] = 100 + counter + c['result']
            codeList.append(c)
            counter += 1
        for key in self.funCode:
            if key != "main":
                funAddr[key] = 100 + counter
                for c in self.funCode[key]:
                    c['addr'] = 100 + counter
                    if c['op'][0] == 'j':
                        try:
                            if c['result'][:3] == 'to_':
                                c['result'] = c['result'][3:]
                                unknownList.append(counter)
                        except:
                            c['result'] = 100 + counter + c['result']
                    codeList.append(c)
                    counter += 1
        for u in unknownList:
            if codeList[u]['result'] == "end":
                codeList[u]['result'] = len(codeList)+ 100
            else:
                codeList[u]['result'] = funAddr[codeList[u]['result']]

        self.codeList = codeList

    def genCode(self, op=None, arg1=None, arg2=None, result=None):
        code = {}
        code['addr'] = 0
        code['op'] = op
        if arg1 != None:
            code['arg1'] = arg1
        if arg2 != None:
            code['arg2'] = arg2
        code['result'] = result
        return code

    def expDFS(self, p):
        if self.error:
            return
        if p.data == "因子":
            if len(p.children) > 1 \
            and p.children[1].data == "FTYPE"\
            and p.children[1].children[0].data == "call":   #过程调用
                symbolIndex, _ = self.lookUpSymbol(
                    p.children[0].children[0].attributes['idName'],
                    self.domain
                )
                if symbolIndex < 0:
                    self.error = True
                    self.errorReason.append("line %d: 未声明的函数 %s" % (
                        p.children[0].children[0].attributes['lineNum'],
                        p.children[0].children[0].attributes['idName']
                    ))
                    return
                tmpCode = []
                tmpParam = []
                self.codeStack.push(tmpCode)
                self.paramStack.push(tmpParam)
                self.expDFS(p.children[1].children[0].children[1])
                if self.error: return
                tmpCode = self.codeStack.pop()
                tmpParam = self.paramStack.pop()
                paramCount = 0
                for s in self.symbolList:
                    if s['domain'] == self.symbolList[symbolIndex]['idName']\
                    and s['label'] == 'formal':
                        paramCount += 1
                if paramCount != len(tmpParam):          #参数个数不匹配
                    self.error = True
                    self.errorReason.append("line %d: %s函数不接受%d个参数"%(
                        p.children[0].children[0].attributes['lineNum'],
                        self.symbolList[symbolIndex]['idName'],
                        len(tmpParam)
                    ))
                for i in range(len(tmpParam)):
                    tmpCode.append(self.genCode(
                        op='push',
                        result=tmpParam[i],
                    ))
                tmpCode.append(self.genCode(
                    op='jal',
                    result="to_" + self.symbolList[symbolIndex]['idName']
                ))
                if self.symbolList[symbolIndex]['label'] == 'formal':
                    p.addAttributes(
                        "place",
                        {'reg': self.symbolList[symbolIndex]['reg']}
                    )
                elif self.symbolList[symbolIndex]['label'] == 'func':
                    code = self.genCode(op='pop', result={'reg':self.newReg()})
                    tmpCode.append(code)
                    p.addAttributes(
                        "place",
                        code['result']
                    )
                else:
                    p.addAttributes(
                        "place",
                        {'symbolIndex':symbolIndex}
                    )
                self.codeStack.top().extend(tmpCode)
                return

            if p.children[0].data == "ID":
                symbolIndex, tag = self.lookUpSymbol(
                    p.children[0].children[0].attributes['idName'],
                    self.domain
                )
                if symbolIndex < 0 or (tag != self.domain and tag != "global"):
                    self.error = True
                    self.errorReason.append("line %d: 未声明的标识符 %s"%(
                        p.children[0].children[0].attributes['lineNum'],
                        p.children[0].children[0].attributes['idName']
                    ))
                    return
                if p.children[0].children[0].attributes['idName'][0] == '-':
                    if self.symbolList[symbolIndex]['label'] == 'formal':
                        p.addAttributes(
                            "place",
                            {'reg': -self.symbolList[symbolIndex]['reg']}
                        )
                    else:
                        p.addAttributes(
                            "place",
                            {'symbolIndex':-symbolIndex}
                        )
                else:
                    if self.symbolList[symbolIndex]['label'] == 'formal':
                        p.addAttributes(
                            "place",
                            {'reg': self.symbolList[symbolIndex]['reg']}
                        )
                    else:
                        p.addAttributes(
                            "place",
                            {'symbolIndex':symbolIndex}
                        )
            if p.children[0].data == "num":
                p.addAttributes(
                    "place",
                    {'Imme':p.children[0].attributes['NumValue']}
                )

        for i in range(len(p.children)):
            self.expDFS(p.children[i])
            if self.error: return
        if p.data == '项' or p.data == '加法表达式':
            if 'place' in p.children[0].attributes and 'place' not in p.children[1].attributes:
                p.addAttributes('place', p.children[0].attributes['place'])
            if 'place' in p.children[0].attributes and 'place' in p.children[1].attributes:
                if p.children[1].children[0].data == '-':
                    p.children[1].children[0].data = '+'
                p.addAttributes('place', {'reg':self.newReg()})
                self.codeStack.top().append(self.genCode(
                    op = p.children[1].children[0].data,
                    arg1 = p.children[0].attributes['place'],
                    arg2 = p.children[1].attributes['place'],
                    result = p.attributes['place']
                ))
        if p.data == '项1' or p.data == '加法表达式1':
            if p.children[0].data == 'NULL':
                return
            if p.children[0].data == '-':
                if 'Imme' in p.children[1].attributes['place']:
                    new = self.newReg()
                    code = self.genCode(
                        op='+',
                        arg1={'reg':0},
                        arg2=p.children[1].attributes['place'],
                        result={'reg':new}
                    )
                    self.codeStack.top().append(code)
                    p.children[1].attributes['place'] = {'reg':new}
                code = self.genCode(
                    op='uminus',
                    result=p.children[1].attributes['place']
                )
                self.codeStack.top().append(code)
            if 'place' in p.children[1].attributes and 'place' not in p.children[2].attributes:
                p.addAttributes('place', p.children[1].attributes['place'])
            if 'place' in p.children[1].attributes and 'place' in p.children[2].attributes:
                if p.children[2].children[0].data == '-':
                    p.children[2].children[0].data = '+'
                p.addAttributes('place', {'reg':self.newReg()})
                code = self.genCode(
                    op = p.children[2].children[0].data,
                    arg1 = p.children[1].attributes['place'],
                    arg2 = p.children[2].attributes['place'],
                    result = p.attributes['place']
                )
                p.addAttributes('code', code)
                self.codeStack.top().append(code)
        if p.data == "表达式" and 'place' in p.children[0].attributes:
            p.addAttributes('place', p.children[0].attributes['place'])
        if p.data == "表达式1" and p.children[0].data == 'relop':
            if 'place' in p.children[1].attributes:
                p.addAttributes('place', p.children[1].attributes['place'])
        if p.data == "因子":
            if 'place' not in p.attributes:
                p.addAttributes('place', p.children[1].attributes['place'])
        if p.data == "实参列表":
            self.paramStack.top().append(p.children[0].attributes['place'])
        if p.data == "实参列表1" and p.children[0].data != 'NULL':
            self.paramStack.top().append(p.children[1].attributes['place'])

    def DFS(self, p):
        if self.error:
            return
        if p.data == "声明":
            symbol = {}
            symbol["type"] = p.children[0].data
            symbol["idName"] = p.children[1].children[0].attributes["idName"]
            if symbol["type"] == "int":
                symbol["offset"] =  self.offset
            if p.children[2].children[0].data == "变量声明":
                symbol['label'] = 'data'
                symbol["domain"] = self.domain
                self.offset += 4
            if p.children[2].children[0].data == "函数声明":  #非void型
                self.domain = symbol["idName"]
                symbol['label'] = 'func'
                symbol["domain"] = symbol["idName"]
                self.haveReturn = False
            if p.children[2].data == "函数声明":              #void型
                symbol['label'] = 'func'
                self.domain = symbol["idName"]
                self.haveReturn = True
                symbol['domain'] = symbol["idName"]
            self.symbolList.append(symbol)

        if p.data == "内部变量声明":
            symbol = {}
            symbol["type"] = p.children[0].data
            symbol["idName"] = p.children[1].children[0].attributes["idName"]
            if symbol["type"] == "int":
                symbol["offset"] = self.offset
                self.offset += 4
            if symbol["type"] == "double":
                symbol["offset"] = self.offset
                self.offset += 8
            symbol['label'] = 'data'
            symbol["domain"] = self.domain
            self.symbolList.append(symbol)

        if p.data == "参数":
            symbol = {}
            symbol["type"] = p.children[0].data
            symbol["idName"] = p.children[1].children[0].attributes["idName"]
            if symbol["type"] == "int":
                symbol["offset"] = self.offset
            if symbol["type"] == "double":
                symbol["offset"] = self.offset
            symbol['label'] = "formal"
            symbol["domain"] = self.domain
            code = self.genCode(op='pop', result={'reg':self.newReg()})
            p.addAttributes('code', [code])
            symbol['reg'] = code['result']['reg']
            self.symbolList.append(symbol)

        if p.data == "赋值语句":
            tmpCode = []
            self.codeStack.push(tmpCode)
            self.expDFS(p.children[2])
            if self.error: return

            symbolIndex, tag = self.lookUpSymbol(
                p.children[0].children[0].attributes['idName'],
                self.domain
            )
            if symbolIndex < 0 or (tag != self.domain and tag != "global"):
                self.error = True
                self.errorReason.append("line %d: 未声明的标识符 %s" % (
                    p.children[0].children[0].attributes['lineNum'],
                    p.children[0].children[0].attributes['idName']
                ))
                return
            if self.symbolList[symbolIndex]['label'] == 'formal':
                result = {'reg': self.symbolList[symbolIndex]['reg']}
            else:
                result = {'symbolIndex': symbolIndex}
            self.codeStack.top().append(self.genCode(
                op = ':=',
                arg1 = p.children[2].attributes['place'],
                result = result
            ))
            p.addAttributes('code', self.codeStack.pop())

        elif p.data == "if语句":

            tmpCode = []
            self.codeStack.push(tmpCode)
            self.expDFS(p.children[2])
            if self.error:
                return
            ifcode = self.codeStack.pop()
            ifcode.append(self.genCode(
                op = 'j' + p.children[2].children[1].children[0].children[0].data,
                arg1 = p.children[2].attributes['place'],
                arg2 = p.children[2].children[1].attributes['place'],
                result = 2
            ))
            Unknown = len(ifcode)
            ifcode.append(self.genCode(op='j', result=-1))
            self.DFS(p.children[4])     #搜索if条件成立的语句块
            if self.error:return
            ifcode.extend(p.children[4].attributes['code'])
            self.DFS(p.children[5])     #搜索else下的语句块
            if self.error:return
            code = self.genCode(op='j')
            ifcode.append(code)
            ifcode[Unknown]['result'] = len(p.children[4].attributes['code'])+2
            if 'code' in p.children[5].attributes:
                code['result'] = len(p.children[5].attributes['code']) + 1
                ifcode.extend(p.children[5].attributes['code'])
            else:
                code['result'] = 1
            p.addAttributes('code', ifcode.copy())

        elif p.data == 'while语句':
            tmpCode = []
            self.codeStack.push(tmpCode)
            self.expDFS(p.children[2])
            if self.error:
                return
            whilecode = self.codeStack.pop()
            whilecode.append(self.genCode(
                op = 'j'+p.children[2].children[1].children[0].children[0].data,
                arg1 = p.children[2].attributes['place'],
                arg2 = p.children[2].children[1].attributes['place'],
                result = 2
            ))
            Unknown = len(whilecode)
            whilecode.append(self.genCode(op='j',result=-1))
            self.DFS(p.children[4])  #搜索while条件成立的语句块
            if self.error:return
            whilecode.extend(p.children[4].attributes['code'])
            whilecode.append(self.genCode(op='j', result=-len(whilecode)))
            whilecode[Unknown]['result'] = len(whilecode)-Unknown
            p.addAttributes('code', whilecode)

        elif p.data == "return语句":
            if self.haveReturn == False: self.haveReturn = True
            tmpCode = []
            if p.children[1].children[0].data != ";":      #有返回值
                symbolIndex, _ = self.lookUpSymbol(self.domain, self.domain)
                if self.symbolList[symbolIndex]['type'] == 'void':  # 函数必须有返回值，报错
                    self.error = True
                    self.errorReason.append('line %d: %s函数不能有返回值' % (
                        p.children[0].attributes['lineNum'],
                        self.domain))
                    return
                self.codeStack.push(tmpCode)
                self.expDFS(p.children[1].children[0])
                if self.error:
                    return
                tmpCode = self.codeStack.pop()
                code = self.genCode(op='push', result=p.children[1].children[0].attributes['place'])
                tmpCode.append(code)
            else:                                         #无返回值
                symbolIndex, _ = self.lookUpSymbol(self.domain, self.domain)
                if self.symbolList[symbolIndex]['type'] != 'void':   #函数必须有返回值，报错
                    self.error = True
                    self.errorReason.append('line %d: %s函数必须有返回值'%(
                        p.children[0].attributes['lineNum'],
                        self.domain
                    ))
            tmpCode.append(self.genCode(op='jr', result='$ra'))
            p.addAttributes('code', tmpCode)

        else:
            for i in range(len(p.children)):
                self.DFS(p.children[i])
                if self.error: return
        if p.data == "语句" and 'code' in p.children[0].attributes:
            p.addAttributes('code', p.children[0].attributes['code'])
        if p.data == "语句串":
            p.addAttributes('code', p.children[0].attributes['code'])
            if 'code' in p.children[1].attributes:
                p.attributes['code'].extend(p.children[1].attributes['code'])
        if p.data == "语句串1" and 'code' in p.children[0].attributes:
            p.addAttributes('code', p.children[0].attributes['code'])
            if 'code' in p.children[1].attributes:
                p.attributes['code'].extend(p.children[1].attributes['code'])
        if p.data == "语句块" :
            p.addAttributes('code', p.children[2].attributes['code'])
        if p.data == 'else语句' and p.children[0].data != 'NULL' and 'code' in p.children[1].attributes:
            p.addAttributes('code', p.children[1].attributes['code'])
        if p.data == "形参" and 'code' in p.children[0].attributes:
            p.addAttributes('code', p.children[0].attributes['code'])
        if p.data == "参数列表" and 'code' in p.children[0].attributes:
            p.addAttributes('code', p.children[0].attributes['code'])
            if 'code' in p.children[1].attributes:
                p.attributes['code'].extend(p.children[1].attributes['code'])
        if p.data == "参数列表1" and p.children[0].data != "NULL" and 'code' in p.children[1].attributes:
            p.addAttributes('code', p.children[1].attributes['code'])
            if 'code' in p.children[2].attributes:
                p.attributes['code'].extend(p.children[2].attributes['code'])
        if p.data == "函数声明":
            if self.haveReturn == False:
                self.error = 1
                self.errorReason.append('%s必须返回一个值'%self.domain)
                return
            self.domain = "global"
            if 'code' in p.children[1].attributes:
                p.addAttributes('code', p.children[1].attributes['code'])
            else:
                p.addAttributes('code',[])
            p.attributes['code'].extend(p.children[-1].attributes['code'])
            if p.parent.data == "声明类型":
                idName = p.parent.parent.children[1].children[0].attributes['idName']
                self.funCode[idName] = p.attributes['code']
            else:
                idName = p.parent.children[1].children[0].attributes['idName']
                self.funCode[idName] = p.attributes['code']

            self.funCode[idName][0]['entry'] = idName
        if p.data == "Program":
            if 'main' not in self.funCode:
                self.error = True
                self.errorReason.append("未定义主函数")
                return
            self.arrangeAddr()

    def analyse(self):
        self.DFS(self.treeHead)
        return self.symbolList, self.codeList, '\n'.join(self.errorReason)+'\n'