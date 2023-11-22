import os


def to_decimal(binary_list):
	result = 0
	for digits in binary_list:
		result = (result << 1) | digits
	return result


def problem1(data):
	gamma = to_decimal([1 if [line[i] for line in data].count('1') > len(data)/2 else 0 for i in range(len(data[0]))])
	epsilon = 2 ** len(data[0]) - 1 - gamma
	return gamma * epsilon


def oxygen_generator_rating(data):
	d = data
	index = 0
	while len(d) > 1:
		most_present_bit = 1 if [line[index] for line in d].count('1') >= len(d)/2 else 0
		d = list(filter(lambda line: int(line[index]) == most_present_bit, d))
		index += 1
	return int(d[0], 2)


def CO2_scrubber_rating(data):
	d = data
	index = 0
	while len(d) > 1:
		least_present_bit = 1 if [line[index] for line in d].count('0') > len(d)/2 else 0
		d = list(filter(lambda line: int(line[index]) == least_present_bit, d))
		index += 1
	return int(d[0], 2)


def problem2(data):
	return oxygen_generator_rating(data) * CO2_scrubber_rating(data)


if __name__ == "__main__":
	directory = os.path.abspath(os.path.dirname(__file__))
	with open(os.path.join(directory, "input.txt")) as file:
		data = [line.strip() for line in file]

	print(problem1(data))  # 2648450
	print(problem2(data))  # 2845944
