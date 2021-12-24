import os
from statistics import median

import sys


def problem1(data):
	total = 0
	med = median(data)
	for value in data:
		total += abs(value - med)
	return total


def problem2(data):
	minimum = min(data)
	maximum = max(data)
	min_fuel = sys.maxsize
	search_min = 0

	for search in range(minimum, maximum):
		total = 0
		for value in data:
			total += (abs(value - search) * (abs(value - search) + 1))/2
		if total < min_fuel:
			min_fuel = total
			search_min = search
		#print(search, total)

	#print(search_min)
	return min_fuel


if __name__ == "__main__":
	directory = os.path.abspath(os.path.dirname(__file__))
	with open(os.path.join(directory, "input.txt")) as file:
		data = list(map(int, [line.strip() for line in file][0].split(',')))

	print(problem1(data))  # 336131
	print(problem2(data))  # 92676646
