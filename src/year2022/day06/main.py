import os


def last_repeated_index(substring: str) -> int:
    save = {}
    substring = substring[::-1]  # reverse the string
    for index, char in enumerate(substring):
        if save.get(char) is None:
            save[char] = index
        else:
            return len(substring) - index
    return -1


def problem1(data: str) -> int:
    index = 0
    length = 4

    while True:
        substring = data[index:index + length]
        fri = last_repeated_index(substring)
        if fri < 0:
            return index + length
        index += fri


def problem2(data: str) -> int:
    index = 0
    length = 14

    while True:
        substring = data[index:index + length]
        fri = last_repeated_index(substring)

        if fri < 0:
            return index + length
        index += fri


def main() -> None:
    directory = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(directory, "input.txt")) as file:
        data = [line.strip() for line in file]

    print(problem1(data[0]))  # 1987
    print(problem2(data[0]))  # 3059


if __name__ == "__main__":
    main()
