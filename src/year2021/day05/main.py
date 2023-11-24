import os
from parse import *


def problem1(data):
	board = [[0 for i in range(1000)] for j in range(1000)]

	for line in data:
		x1, y1, x2, y2 = parse('{},{} -> {},{}', line)
		x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
		if x1 > x2:
			x1, x2 = x2, x1
		if y1 > y2:
			y1, y2 = y2, y1

		if x1 == x2:
			for y in range(y1, y2 + 1):
				board[x1][y] += 1

		if y1 == y2:
			for x in range(x1, x2 + 1):
				board[x][y1] += 1

	count = 0
	for i in range(len(board)):
		for j in range(len(board)):
			if board[i][j] >= 2:
				count += 1

	return count


def problem2(data):
	board = [[0 for i in range(1000)] for j in range(1000)]

	for line in data:
		x1, y1, x2, y2 = parse('{},{} -> {},{}', line)
		x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

		if x1 == x2:
			if y1 > y2:
				y1, y2 = y2, y1
			for y in range(y1, y2 + 1):
				board[x1][y] += 1

		elif y1 == y2:
			if x1 > x2:
				x1, x2 = x2, x1
			for x in range(x1, x2 + 1):
				board[x][y1] += 1

		else:
			x_step = 1 if x1 < x2 else - 1
			y_step = 1 if y1 < y2 else - 1
			for x, y in zip(range(x1, x2 + x_step, x_step), range(y1, y2 + y_step, y_step)):
				board[x][y] += 1

	count = 0
	for i in range(len(board)):
		for j in range(len(board)):
			if board[i][j] >= 2:
				count += 1

	return count


if __name__ == "__main__":
	directory = os.path.abspath(os.path.dirname(__file__))
	with open(os.path.join(directory, "input.txt")) as file:
		data = [line.strip() for line in file]

	print(problem1(data))  # 5690
	print(problem2(data))  # 17741
