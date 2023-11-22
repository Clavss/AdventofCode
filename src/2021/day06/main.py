import os


def simulate(data, days):
	fishes = data.copy()

	occurences = []
	for i in range(9):
		occurences.append(fishes.count(i))

	for day in range(days):
		#print(day, occurences)
		save = occurences[0]
		for i in range(len(occurences) - 1):
			occurences[i] = occurences[i + 1]
		occurences[6] += save
		occurences[8] = save

	#print(days, occurences)
	return sum(occurences)


def problem1(data):
	return simulate(data, 80)


def problem2(data):
	return simulate(data, 256)


if __name__ == "__main__":
	directory = os.path.abspath(os.path.dirname(__file__))
	with open(os.path.join(directory, "input.txt")) as file:
		data = list(map(int, [line.strip() for line in file][0].split(',')))

	print(problem1(data))  # 387413
	print(problem2(data))  # 1738377086345
