import copy
import os

import itertools


def sub_flash(data, i, j):
	if data[i][j] != -1 and data[i][j] < 9:
		data[i][j] += 1
	elif data[i][j] == 9:
		flash(data, i, j)


def flash(data, i, j):
	data[i][j] = -1
	for x, y in itertools.product(range(-1, 2), range(-1, 2)):
		if 0 <= i+x < len(data) and 0 <= j+y < len(data[0]):
			sub_flash(data, i+x, j+y)


def problem1(data):
	flash_count = 0
	for step in range(100):
		for i, j in itertools.product(range(len(data)), range(len(data[0]))):
			sub_flash(data, i, j)

		for i, j in itertools.product(range(len(data)), range(len(data[0]))):
			if data[i][j] == -1:
				data[i][j] = 0
				flash_count += 1

	return flash_count


def problem2(data):
	flash_count = 0
	step = 0
	while flash_count != len(data) * len(data[0]):
		flash_count = 0
		step += 1

		for i, j in itertools.product(range(len(data)), range(len(data[0]))):
			sub_flash(data, i, j)

		for i, j in itertools.product(range(len(data)), range(len(data[0]))):
			if data[i][j] == -1:
				data[i][j] = 0
				flash_count += 1

	return step


if __name__ == "__main__":
	directory = os.path.abspath(os.path.dirname(__file__))
	with open(os.path.join(directory, "input.txt")) as file:
		data1 = [list(map(int, list(line.strip()))) for line in file]
		data2 = copy.deepcopy(data1)

	print(problem1(data1))  # 1735
	print(problem2(data2))  # 400
