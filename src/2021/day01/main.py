import os


def problem1(data):
	return [data[i + 1] > data[i] for i in range(len(data) - 1)].count(True)


def problem2(data):
	return problem1([data[i] + data[i + 1] + data[i + 2] for i in range(len(data) - 2)])


if __name__ == "__main__":
	directory = os.path.abspath(os.path.dirname(__file__))
	with open(os.path.join(directory, "input.txt")) as file:
		data = [int(line.strip()) for line in file]

	print(problem1(data))  # 1665
	print(problem2(data))  # 1702
