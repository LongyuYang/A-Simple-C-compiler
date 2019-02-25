

'''产生式类'''
class Production:

    def __init__(self, left=None, right=None):
        self.left = left      #左部
        self.right = right    #右部

'''产生式表类'''
class ProductionList:
    def __init__(self):
        self.List = []
        self.start = ''

    def __getitem__(self, item):
        return self.List[item]

    def __len__(self):
        return len(self.List)

    '''判断产生式p是否存在'''
    def isExist(self, p):
        for i in self.List:
            if p.left == i.left and p.right == i.right:
                return True
        return False

    '''加入一个产生式p'''
    def add(self, p):
        if self.isExist(p) == False:
            self.List.append(p)

    '''删除产生式p'''
    def delete(self, p):
        for i in self.List:
            if p.left == i.left and p.right == i.right:
                self.List.remove(i)
                break

    '''返回左部为Virable的产生式'''
    def getVirablePro(self, Virable):
        results = []
        for p in self.List:
            if p.left == Virable:
                results.append(p)
        return results

def getCPro():

    inputPro = [['Program', ['声明串']],
                ['声明串', ['声明']],
                ['声明串', ['声明串', '声明']],
                ['声明', ['int', 'ID', '声明类型']],
                ['声明', ['void', 'ID', '函数声明']],
                ['声明类型', ['变量声明']],
                ['声明类型', ['函数声明']],
                ['变量声明', [';']],
                ['函数声明', ['(', '形参', ')', '语句块']],
                ['形参', ['参数列表']],
                ['形参', ['void']],
                ['参数列表', ['参数']],
                ['参数列表', ['参数列表', ',', '参数']],
                ['参数', ['int', 'ID']],
                ['语句块', ['{', '内部声明',  '语句串', '}']],
                ['内部声明', ['NULL']],
                ['内部声明', ['内部声明',  '内部变量声明',';']],      #change
                ['内部变量声明', ['int', 'ID']],
                ['内部变量声明', ['double', 'ID']],     #add
                ['语句串', ['语句']],
                ['语句串', ['语句串', '语句']],
                ['语句', ['if语句']],
                ['语句', ['while语句']],
                ['语句', ['return语句']],
                ['语句', ['赋值语句']],
                ['赋值语句', ['ID', '=', '表达式', ';']],
                ['return语句', ['return', '返回值']],
                ['返回值', ['表达式',';']],     #change
                ['返回值', [';']],             #change
                ['while语句', ['while', '(', '表达式', ')', '语句块']],
                ['if语句', ['if', '(', '表达式', ')', '语句块', 'else语句']],
                ['else语句', ['else', '语句块']],
                ['else语句', ['NULL']],
                ['表达式', ['加法表达式']],
                ['表达式', ['表达式', 'relop', '加法表达式']],
                ['relop', ['<']],
                ['relop', ['<=']],
                ['relop', ['>']],
                ['relop', ['>=']],
                ['relop', ['==']],
                ['relop', ['!=']],
                ['加法表达式', ['项']],
                ['加法表达式', ['加法表达式', '+', '项']],
                ['加法表达式', ['加法表达式', '-', '项']],
                ['项', ['因子']],
                ['项', ['项', '*', '因子']],
                ['项', ['项', '/', '因子']],
                ['因子', ['num']],
                ['因子', ['(', '表达式', ')']],
                ['因子', ['ID', 'FTYPE']],
                ['FTYPE', ['call']],
                ['FTYPE', ['NULL']],
                ['call', ['(', '实参列表', ')']],
                ['实参', ['实参列表']],
                ['实参', ['NULL']],
                ['实参列表', ['表达式']],
                ['实参列表', ['实参列表', ',', '表达式']],
                ['ID', ['标识符']]]
    '''
    inputPro = [['E', ['E', '+', 'T']],
                     ['E', ['T']],
                     ['T', ['T', '*', 'F']],
                     ['T', ['F']],
                     ['F', ['(', 'E', ')']],
                     ['F', ['i']]]
    '''
    '''
    inputPro = [['S',['a']],
                ['S',['^']],
                ['S',['(','T',')']],
                ['T',['T',',','S']],
                ['T',['S']]]
    Terminals = ['a','^','(',')',',']
    '''
    '''
    inputPro = [['E',['T','E1']],
                ['E1',['+','E']],
                ['E1',['NULL']],
                ['T',['F','T1']],
                ['T1',['T']],
                ['T1',['NULL']],
                ['F',['P','F1']],
                ['F1',['*','F1']],
                ['F1',['NULL']],
                ['P',['(','E',')']],
                ['P',['a']],
                ['P', ['b']],
                ['P', ['^']]]
    Terminals = ['+','*','^','(',')','a','b']
    '''
    '''
    inputPro = [['S',['Q','c']],
                ['S',['c']],
                ['Q',['R','b']],
                ['Q',['b']],
                ['R',['S','a']],
                ['R',['a']]]
    '''
    return inputPro