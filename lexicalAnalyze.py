class LexAn:
	keywords = ["int", "void", "if", "else", "while", "return", "double"]

	def __init__(self, text):
		self.text = text

	def lex_analyze(self, i):
		j = i
		text=self.text
		if text[i] == '#':
			return j, "结束符"
		elif text[i].isalpha():
			j += 1
			while text[j].isalpha() or text[j].isdigit():
				j += 1
			if text[i:j] in self.keywords:
				return j - 1, "关键字"
			else:
				return j - 1, "标识符"
		elif text[i].isdigit():
			j += 1
			while text[j].isdigit():
				j += 1
			return j - 1, "数值"
		elif text[i] == '=':
			j += 1
			if text[j] == '=':
				return j, "算符"
			else:
				return j - 1, "赋值号"
		elif text[i] == '/':
			j += 1
			if text[j] == '/':
				while text[j] != '\n':
					j += 1
					if text[j] == '#':
						return j - 1, "注释号"
				return j - 1, "注释号"
			elif text[j] == '*':
				j += 1
				if text[j] == '#':
					return j - 1, "ERROR"
				if text[j + 1] == '#':
					return j, "ERROR"
				while text[j] != '*' or text[j + 1] != '/':
					j += 1
					if text[j] == '#':
						return j - 1, "ERROR"
					if text[j + 1] == '#':
						return j, "ERROR"
				return j + 1, "注释号"
			else:
				return j - 1, "算符"
		elif text[i] == '+' or text[i] == '-' or text[i] == '*':
			return j, "算符"
		elif text[i] == '>' or text[i] == '<':
			j += 1
			if text[j] == '=':
				return j, "算符"
			else:
				return j - 1, "算符"
		elif text[i] == '!':
			j += 1
			if text[j] == '=':
				return j, "算符"
			else:
				return j - 1, "ERROR"
		elif text[i] == ';':
			return j, "界符"
		elif text[i] == ',':
			return j, "分隔符"
		elif text[i] == '(':
			return j, "左括号"
		elif text[i] == ')':
			return j, "右括号"
		elif text[i] == '{':
			return j, "左大括号"
		elif text[i] == '}':
			return j, "右大括号"
		else:
			return j, "ERROR"
