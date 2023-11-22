import os

from itertools import chain


def problem1(data):
	outputs = []
	for line in data:
		outputs.append(line.split('| ', 1)[1].split(' '))
	outputs = list(chain.from_iterable(outputs))

	return len(list(filter(lambda word: len(word) <= 4 or len(word) == 7, outputs)))

# digit (number of segments):
# 0 (6)
# 1 (2) --> unique
# 2 (5)
# 3 (5)
# 4 (4) --> unique
# 5 (5)
# 6 (6)
# 7 (3) --> unique
# 8 (7) --> unique
# 9 (6)

# with the above: numbers 1, 4, 7 and 8 are known

#   a
# b   c
#   d
# e   f
#   g

# line (occurence in digits) --> how to find it
# a (8) --> 7-1
# b (6) --> unique
# c (8) --> 1-f
# d (7) --> 4-bcf
# e (4) --> unique
# f (9) --> unique
# g (7) --> last


def problem2(data):
	total = 0

	for line in data:
		inputs = list(chain.from_iterable([line.split(' |', 1)[0].split(' ')]))
		outputs = list(chain.from_iterable([line.split('| ', 1)[1].split(' ')]))

		digits = {'1': ''.join(sorted(list(filter(lambda input_str: len(input_str) == 2, inputs))[0])),
				  '4': ''.join(sorted(list(filter(lambda input_str: len(input_str) == 4, inputs))[0])),
				  '7': ''.join(sorted(list(filter(lambda input_str: len(input_str) == 3, inputs))[0])),
				  '8': ''.join(sorted(list(filter(lambda input_str: len(input_str) == 7, inputs))[0]))}

		occurences = {'4': list(filter(lambda input_str: [i for ele in inputs for i in ele].count(input_str) == 4, [i for ele in inputs for i in ele]))[0],
					  '6': list(filter(lambda input_str: [i for ele in inputs for i in ele].count(input_str) == 6, [i for ele in inputs for i in ele]))[0],
					  '9': list(filter(lambda input_str: [i for ele in inputs for i in ele].count(input_str) == 9, [i for ele in inputs for i in ele]))[0]}

		letters = {'a': substract(digits['7'], digits['1']),
				   'b': occurences['6'],
				   'e': occurences['4'],
				   'f': occurences['9']}
		letters['c'] = substract(digits['1'], letters['f'])
		letters['d'] = substract(substract(substract(digits['4'], letters['b']), letters['c']), letters['f'])
		letters['g'] = substract(substract(substract(substract(substract(substract('abcdefg', letters['a']), letters['b']), letters['c']), letters['d']), letters['e']), letters['f'])

		final_dict = {'abcefg': 0,
					  'cf': 1,
					  'acdeg': 2,
					  'acdfg': 3,
					  'bcdf': 4,
					  'abdfg': 5,
					  'abdefg': 6,
					  'acf': 7,
					  'abcdefg': 8,
					  'abcdfg': 9}

		total += int(''.join([str(final_dict[x]) for x in [equi(outputs_str, letters) for outputs_str in outputs]]))
	return total


def equi(outputs_str, letters_dict):
	res = ''
	for letter in outputs_str:
		res += list(letters_dict.keys())[list(letters_dict.values()).index(letter)][0]
	return ''.join(sorted(res))


def substract(str1, str2):
	res = str1
	for letter in str2:
		res = res.replace(letter, '')
	return res


if __name__ == "__main__":
	directory = os.path.abspath(os.path.dirname(__file__))
	with open(os.path.join(directory, "input.txt")) as file:
		data = [line.strip() for line in file]

	print(problem1(data))  # 519
	print(problem2(data))  # 1027483
