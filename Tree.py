
class node:
    def __init__(self):
        self.parent = None
        self.children = []
        self.data = None
        self.attributes = {}

    def setData(self, data):
        self.data = data

    def setParent(self, parent):
        self.parent = parent

    def addChildren(self, child):
        self.children.append(child)

    def reverseChildren(self):
        tmp = self.children.copy()
        self.children = []
        i = len(tmp) - 1
        while (i >= 0):
            self.children.append(tmp[i])
            i -= 1

    def addAttributes(self, name, value):
        self.attributes[name] = value