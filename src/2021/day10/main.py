import os


def correspond(s1, s2):
	return '([{<'.index(s2) == ')]}>'.index(s1)


def sym_error_value(sym):
	sym_value_dict = {')': 3,
					  ']': 57,
					  '}': 1197,
					  '>': 25137}
	return sym_value_dict[sym]


def sym_error(line):
	sym_open = '([{<'
	sym_close = ')]}>'
	stack = []

	for symbol in line:
		if symbol in sym_open:
			stack.append(symbol)
		elif symbol in sym_close:
			if len(stack) == 0 or not correspond(symbol, stack.pop()):
				return sym_error_value(symbol)
	return 0


def problem1(data):
	return sum([sym_error(line) for line in data])


def sym_incomplete(line):
	sym_open = '([{<'
	sym_close = ')]}>'
	stack = []

	for symbol in line:
		if symbol in sym_open:
			stack.append(symbol)
		elif symbol in sym_close:
			if len(stack) == 0 or not correspond(symbol, stack.pop()):
				return ''
	return ''.join(stack[::-1])


def replace_by_correspond(line_completion):
	sym_open = '([{<'
	sym_close = ')]}>'
	res = ''
	for symbol in line_completion:
		res += sym_close[sym_open.index(symbol)]
	return res


def line_score(line_completion):
	value = {')': 1,
			 ']': 2,
			 '}': 3,
			 '>': 4}
	score = 0
	for symbol in line_completion:
		score = score * 5 + value[symbol]
	return score


def problem2(data):
	scores = list(filter(lambda score: score > 0, [line_score(replace_by_correspond(sym_incomplete(line))) for line in data]))
	return sorted(scores)[len(scores)//2]


if __name__ == "__main__":
	directory = os.path.abspath(os.path.dirname(__file__))
	with open(os.path.join(directory, "input.txt")) as file:
		data = [line.strip() for line in file]

	print(problem1(data))  # 413733
	print(problem2(data))  # 3354640192
