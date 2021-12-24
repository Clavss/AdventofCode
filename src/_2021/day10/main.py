import os


def problem1(data):
	pass


def problem2(data):
	pass


if __name__ == "__main__":
	directory = os.path.abspath(os.path.dirname(__file__))
	with open(os.path.join(directory, "input.txt")) as file:
		data = [line.strip() for line in file]

	print(problem1(data))  # ?
	print(problem2(data))  # ?
