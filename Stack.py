from Tree import node

class MyStack:
    def __init__(self):
        self.s = []

    def push(self, e):
        self.s.append(e)

    def pop(self):
        e = self.s[-1]
        del self.s[-1]
        return e

    def top(self):
        return self.s[-1]

    def show(self):
        result = []
        for t in self.s:
            result.append(t.data)
        return (' '.join(result))

    def __len__(self):
        return len(self.s)