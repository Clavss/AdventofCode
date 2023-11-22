import os


class Board:
	def __init__(self):
		self.values = []

	def replace(self, number):
		for i in range(len(self.values)):
			for j in range(len(self.values[i])):
				if self.values[i][j] == number:
					self.values[i][j] = 0

	def check_bingo(self, number):
		self.replace(number)
		return [sum(i for i in row) for row in self.values] + [sum(v) for i, v in enumerate(zip(*self.values))]

	def display(self):
		print()
		for row in self.values:
			print(row)

	def add_row(self, row):
		self.values.append(row)


def make_board(data):
	drown = [int(number) for number in data[0].split(',')]
	boards = []
	for i in range(2, len(data), 6):
		board = Board()
		for j in range(5):
			board.add_row([int(value) for value in data[i+j].split()])
		boards.append(board)

	return drown, boards


def problem1(data):
	drown, boards = make_board(data)
	for number in drown:
		for board in boards:
			#board.display()
			check = board.check_bingo(number)
			if check.count(0):
				return sum(check) / 2 * number


def problem2(data):
	drown, boards = make_board(data)

	for number in drown:
		i = 0
		deleted = []

		while i < len(boards):
			#print('-----------------------')
			#print(number, i, len(boards))
			#boards[i].display()
			check = boards[i].check_bingo(number)

			if check.count(0):
				#boards[i].display()
				if len(boards) == 1:
					return sum(check) / 2 * number
				deleted.append(i)
				#print('DEL')
			i += 1

		for ele in sorted(deleted, reverse=True):
			del boards[ele]


if __name__ == "__main__":
	directory = os.path.abspath(os.path.dirname(__file__))
	with open(os.path.join(directory, "input.txt")) as file:
		data = [line.strip() for line in file]

	print(problem1(data))  # 32844
	print(problem2(data))  # 4920
