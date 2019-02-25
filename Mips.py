
class Assembler():
    def __init__(self, symbolList, codeList):
        self.mipsList = []
        self.symbolList = symbolList
        self.codeList = codeList
        self.entryCount = -1
        self.entryTable = {}
        self.maps = {}

    def dataInit(self):
        self.mipsList.append('.data\n')
        for s in self.symbolList:
            if s['label'] == 'data':
                newLine = s['idName']+'_'+s['domain']+":"
                if s['type'] == 'int':
                    newLine += '\t.word\t0\n'
                self.mipsList.append(newLine)

    def newEntry(self):
        self.entryCount += 1
        return 'L'+str(self.entryCount)

    def getEntry(self, c):
        entryTable = self.entryTable
        if c['result'] > c['addr'] and 'newEntry' not in self.codeList[c['result'] - 100]:
            newEntry = self.newEntry()
            self.codeList[c['result'] - 100]['newEntry'] = newEntry
            entryTable[c['result']] = newEntry
        elif c['result'] > c['addr'] and 'newEntry' in self.codeList[c['result'] - 100]:
            newEntry = self.codeList[c['result'] - 100]['newEntry']
        elif c['result'] < c['addr'] and c['result'] not in entryTable:
            newEntry = self.newEntry()
            self.mipsList[self.maps[c['result']]] = newEntry + ':\n' + self.mipsList[self.maps[c['result']]]
            entryTable[c['result']] = newEntry
        elif c['result'] < c['addr'] and c['result'] in entryTable:
            newEntry = entryTable[c['result']]
        return newEntry

    def getArgs(self, c):
        before = ""
        after = ""
        if 'arg1' in c:
            if 'symbolIndex' in c['arg1']:
                arg1 = '$24'
                index = c['arg1']['symbolIndex']
                before += 'lw $24, '
                name = self.symbolList[index]['idName'] + '_' + self.symbolList[index]['domain']
                before += (name + '\n')
            elif 'reg' in c['arg1']:
                arg1 = '$%d' % c['arg1']['reg']
            else:
                arg1 = c['arg1']['Imme']
        else:
            arg1 = ""
        if 'arg2' in c:
            if 'symbolIndex' in c['arg2']:
                arg2 = '$25'
                before += 'lw $25, '
                index = c['arg2']['symbolIndex']
                name = self.symbolList[index]['idName'] + '_' + self.symbolList[index]['domain']
                before += (name + '\n')
            elif 'reg' in c['arg2']:
                arg2 = '$%d' % c['arg2']['reg']
            else:
                arg2 = c['arg2']['Imme']
        else:
            arg2 = ""
        if c['op'][0] != 'j':
            if 'symbolIndex' in c['result']:
                result = '$26'
                if c['op'] != 'push':
                    after += 'sw $26, '
                    index = c['result']['symbolIndex']
                    name = self.symbolList[index]['idName'] + '_' + self.symbolList[index]['domain']
                    after += (name + '\n')
                else:
                    before += 'lw $26, '
                    index = c['result']['symbolIndex']
                    name = self.symbolList[index]['idName'] + '_' + self.symbolList[index]['domain']
                    before += (name + '\n')
            elif 'reg' in c['result']:
                result = '$%d' % c['result']['reg']
            else:
                result = ""
        else:
            result = ""
        return arg1, arg2, result, before, after

    def getText(self):
        self.mipsList.append('\n.text\n')
        self.mipsList.append('addi $sp, $0, 0x10018000\t#初始化栈顶\n')
        for c in self.codeList:
            line = ""
            if 'entry' in c:
                line += ('\n\n'+c['entry']+':\n')
            if 'newEntry' in c:
                line += (c['newEntry']+':\n')
            if c['op'] == ':=':
                arg1, _, result, before, after = self.getArgs(c)
                line += before
                if arg1[0] != '$':
                    line += ('addi '+result+', $0, '+arg1+'\n')
                else:
                    line += ('add ' + result + ', $0, ' + arg1 + '\n')
                line += after
            elif c['op'] == 'push':
                _, _, result, before, after = self.getArgs(c)
                line += before
                line += ('sw '+result+', 0($sp)\n')
                line += ('addi $sp, $sp, 4\n')
            elif c['op'] == 'pop':
                _, _, result, before, after = self.getArgs(c)
                line += ('lw '+result+', -4($sp)\n')
                line += ('sub $sp, $sp, 4\n')
            elif c['op'] == 'jr':
                if c['result'] == 'end':
                    line += ('j end\n')
                else:
                    line += ('jr $ra\n')
            elif c['op'] == 'jal':
                line += ('jal '+self.codeList[c['result']-100]['entry']+'\n')
            elif c['op'] == 'j':
                line += ('j '+self.getEntry(c)+'\n')
            elif c['op'] == 'j>':
                newEntry = self.getEntry(c)
                arg1, arg2, _, before, after = self.getArgs(c)
                line += before
                if arg1[0] != '$' and arg2[0] == '$':
                    line += ('bgt ' + arg2+', '+arg1+', '+newEntry + '\n')
                if arg1[0] == '$' and arg2[0] != '$':
                    line += ('bgt ' + arg1 + ', ' + arg2 + ', ' + newEntry + '\n')
                if arg1[0] == '$' and arg2[0] == '$':
                    line += ('bgt ' + arg1 + ', ' + arg2 + ', ' + newEntry + '\n')
            elif c['op'] == 'j>=':
                newEntry = self.getEntry(c)
                arg1, arg2, _, before, after = self.getArgs(c)
                line += before
                if arg1[0] != '$' and arg2[0] == '$':
                    line += ('bge ' + arg2+', '+arg1+', '+newEntry + '\n')
                if arg1[0] == '$' and arg2[0] != '$':
                    line += ('bge ' + arg1 + ', ' + arg2 + ', ' + newEntry + '\n')
                if arg1[0] == '$' and arg2[0] == '$':
                    line += ('bge ' + arg1 + ', ' + arg2 + ', ' + newEntry + '\n')
            elif c['op'] == 'j<':
                newEntry = self.getEntry(c)
                arg1, arg2, _, before, after = self.getArgs(c)
                line += before
                if arg1[0] != '$' and arg2[0] == '$':
                    line += ('blt ' + arg2+', '+arg1+', '+newEntry + '\n')
                if arg1[0] == '$' and arg2[0] != '$':
                    line += ('blt ' + arg1 + ', ' + arg2 + ', ' + newEntry + '\n')
                if arg1[0] == '$' and arg2[0] == '$':
                    line += ('blt ' + arg1 + ', ' + arg2 + ', ' + newEntry + '\n')
            elif c['op'] == 'j<=':
                newEntry = self.getEntry(c)
                arg1, arg2, _, before, after = self.getArgs(c)
                line += before
                if arg1[0] != '$' and arg2[0] == '$':
                    line += ('ble ' + arg2+', '+arg1+', '+newEntry + '\n')
                if arg1[0] == '$' and arg2[0] != '$':
                    line += ('ble ' + arg1 + ', ' + arg2 + ', ' + newEntry + '\n')
                if arg1[0] == '$' and arg2[0] == '$':
                    line += ('ble ' + arg1 + ', ' + arg2 + ', ' + newEntry + '\n')
            elif c['op'] == 'j==':
                newEntry = self.getEntry(c)
                arg1, arg2, _, before, after = self.getArgs(c)
                line += before
                if arg1[0] != '$' and arg2[0] == '$':
                    line += ('beq ' + arg2+', '+arg1+', '+newEntry + '\n')
                if arg1[0] == '$' and arg2[0] != '$':
                    line += ('beq ' + arg1 + ', ' + arg2 + ', ' + newEntry + '\n')
                if arg1[0] == '$' and arg2[0] == '$':
                    line += ('beq ' + arg1 + ', ' + arg2 + ', ' + newEntry + '\n')
            elif c['op'] == 'j!=':
                newEntry = self.getEntry(c)
                arg1, arg2, _, before, after = self.getArgs(c)
                line += before
                if arg1[0] != '$' and arg2[0] == '$':
                    line += ('bne ' + arg2+', '+arg1+', '+newEntry + '\n')
                if arg1[0] == '$' and arg2[0] != '$':
                    line += ('bne ' + arg1 + ', ' + arg2 + ', ' + newEntry + '\n')
                if arg1[0] == '$' and arg2[0] == '$':
                    line += ('bne ' + arg1 + ', ' + arg2 + ', ' + newEntry + '\n')
            elif c['op'] == '+':
                arg1, arg2, result, before, after = self.getArgs(c)
                line += before
                if arg1[0] == '$' and arg2[0] != '$':
                    line += ('addi '+result+', '+arg1+', '+arg2+'\n')
                if arg1[0] != '$' and arg2[0] == '$':
                    line += ('addi ' + result + ', ' + arg2 + ', ' + arg1 + '\n')
                if arg1[0] == '$' and arg2[0] == '$':
                    line += ('add ' + result + ', ' + arg1 + ', ' + arg2 + '\n')
                if arg1[0] != '$' and arg2[0] != '$':
                    line += ('addi $24, $0, ' + arg1 + '\n')
                    line += ('addi ' + result + ', $24, ' + arg2 + '\n')
                line += after
            elif c['op'] == '*':
                arg1, arg2, result, before, after = self.getArgs(c)
                line += before
                if arg1[0] == '$' and arg2[0] != '$':
                    line += ('mul '+result+', '+arg1+', '+arg2+'\n')
                if arg1[0] != '$' and arg2[0] == '$':
                    line += ('mul ' + result + ', ' + arg2 + ', ' + arg1 + '\n')
                if arg1[0] == '$' and arg2[0] == '$':
                    line += ('mul ' + result + ', ' + arg1 + ', ' + arg2 + '\n')
                if arg1[0] != '$' and arg2[0] != '$':
                    line += ('mul $24, $0, ' + arg1 + '\n')
                    line += ('mul ' + result + ', $24, ' + arg2 + '\n')
                line += after
            elif c['op'] == '/':
                arg1, arg2, result, before, after = self.getArgs(c)
                line += before
                if arg1[0] == '$' and arg2[0] != '$':
                    line += ('div '+result+', '+arg1+', '+arg2+'\n')
                if arg1[0] != '$' and arg2[0] == '$':
                    line += ('div ' + result + ', ' + arg2 + ', ' + arg1 + '\n')
                if arg1[0] == '$' and arg2[0] == '$':
                    line += ('div ' + result + ', ' + arg1 + ', ' + arg2 + '\n')
                if arg1[0] != '$' and arg2[0] != '$':
                    line += ('div $24, $0, ' + arg1 + '\n')
                    line += ('div ' + result + ', $24, ' + arg2 + '\n')
                line += after
            elif c['op'] == 'uminus':
                arg1, arg2, result, before, after = self.getArgs(c)
                line += before

                if result[0] == '$':
                    line += ('sub ' + result + ', $0, ' + result + '\n')
                else:
                    line += ('subi ' + result + ', $0, ' + result + '\n')
                line += after
            self.maps[c['addr']] = len(self.mipsList)

            self.mipsList.append(line)
        self.mipsList.append('end:')

    def generate(self):
        self.dataInit()
        self.getText()
        return ''.join(self.mipsList)