import os


class Submarine:
	def __init__(self):
		self.horizontal = 0
		self.depth = 0
		self.aim = 0

	def add_horizontal(self, x):
		self.horizontal += x

	def add_depth(self, y):
		self.depth += y

	def forward(self, value):
		self.horizontal += value
		self.depth += self.aim * value

	def down(self, value):
		self.aim += value

	def up(self, value):
		self.aim -= value

	def result(self):
		return self.horizontal * self.depth


def problem1(data):
	submarine = Submarine()

	for line in data:
		command, value = line.split(' ')
		value = int(value)
		if command == 'forward':
			submarine.add_horizontal(value)
		elif command == 'down':
			submarine.add_depth(value)
		elif command == 'up':
			submarine.add_depth(-value)

	return submarine.result()


def problem2(data):
	submarine = Submarine()

	for line in data:
		command, value = line.split(' ')
		value = int(value)
		if command == 'forward':
			submarine.forward(value)
		elif command == 'down':
			submarine.down(value)
		elif command == 'up':
			submarine.up(value)

	return submarine.result()


if __name__ == "__main__":
	directory = os.path.abspath(os.path.dirname(__file__))
	with open(os.path.join(directory, "input.txt")) as file:
		data = [line.strip() for line in file]

	print(problem1(data))  # 1648020
	print(problem2(data))  # 1759818555
