import math
import os

import itertools


def get_adjacent_points(data, i, j):
	adjacent_points = []
	if i > 0:
		adjacent_points.append((i - 1, j))
	if j > 0:
		adjacent_points.append((i, j - 1))
	if j < len(data[0]) - 1:
		adjacent_points.append((i, j + 1))
	if i < len(data) - 1:
		adjacent_points.append((i + 1, j))
	return adjacent_points


def problem1(data):
	low_points = []
	for i, j in itertools.product(range(len(data)), range(len(data[0]))):
		adjacent_points = get_adjacent_points(data, i, j)

		if [True if int(data[i][j]) < int(data[point[0]][point[1]]) else False for point in adjacent_points].count(False) == 0:
			low_points.append(int(data[i][j]) + 1)

	return sum(low_points)


def navigate(data, point):
	i, j = point
	if int(data[i][j]) == 9:
		return 0
	else:
		data[i] = data[i][:j] + '9' + data[i][j + 1:]

	adjacent_points = get_adjacent_points(data, i, j)

	return 1 + sum([navigate(data, point) for point in adjacent_points])


def problem2(data):
	basins_length = [navigate(data, (i, j)) for i, j in itertools.product(range(len(data)), range(len(data[0])))]
	basins_length.sort()
	return math.prod(basins_length[-3:])


if __name__ == "__main__":
	directory = os.path.abspath(os.path.dirname(__file__))
	with open(os.path.join(directory, "input.txt")) as file:
		data = [line.strip() for line in file]

	print(problem1(data))  # 535
	print(problem2(data))  # 1122700
