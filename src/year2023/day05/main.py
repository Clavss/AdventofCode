import math
import os
import re

from utils.exercise import Exercise


def parse_ints(line: str) -> list[int]:
    numbers = [int(m) for m in re.findall(r'\d+', line)]
    return numbers


class Problem(Exercise):

    def part1(self, data: list[str]) -> int | str:
        index: int = 3
        seeds: list[int] = parse_ints(data[0])
        seed_to_soil: list[list[int]] = []
        seed_to_fertilizer: list[list[int]] = []
        fertilizer_to_water: list[list[int]] = []
        water_to_light: list[list[int]] = []
        light_to_temperature: list[list[int]] = []
        temperature_to_humidity: list[list[int]] = []
        humidity_to_location: list[list[int]] = []
        maps: list[list[list[int]]] = [seed_to_soil, seed_to_fertilizer, fertilizer_to_water, water_to_light,
                                       light_to_temperature, temperature_to_humidity, humidity_to_location]

        for _map in maps:
            for line in data[index::]:
                index += 1
                if line == '':
                    index += 1
                    break
                _map.append(parse_ints(line))

        res = math.inf
        for seed in seeds:
            value = seed
            for _map in maps:
                for dest, source, length in _map:
                    if source <= value < source + length:
                        value += dest - source
                        break

            res = min(res, value)

        return res

    def part2(self, data: list[str]) -> int | str:
        index: int = 3
        inputs: list[int] = parse_ints(data[0])
        seeds: list[tuple[int, int]] = []
        seed_to_soil: list[list[int]] = []
        seed_to_fertilizer: list[list[int]] = []
        fertilizer_to_water: list[list[int]] = []
        water_to_light: list[list[int]] = []
        light_to_temperature: list[list[int]] = []
        temperature_to_humidity: list[list[int]] = []
        humidity_to_location: list[list[int]] = []
        maps: list[list[list[int]]] = [seed_to_soil, seed_to_fertilizer, fertilizer_to_water, water_to_light,
                                       light_to_temperature, temperature_to_humidity, humidity_to_location]

        for _map in maps:
            for line in data[index::]:
                index += 1
                if line == '':
                    index += 1
                    break
                _map.append(parse_ints(line))

        for index in range(0, len(inputs), 2):
            seeds_range_start = inputs[index]
            seeds_range_length = inputs[index + 1]
            seeds.append((seeds_range_start, seeds_range_start + seeds_range_length))

        for _map in maps:
            next_values = []
            while len(seeds) > 0:
                seed_range_start, seed_range_end = seeds.pop()
                for dest, source, length in _map:
                    mapping = dest - source
                    overlap_range_start = max(seed_range_start, source)
                    overlap_range_end = min(seed_range_end, source + length)
                    # found a mapping
                    if overlap_range_start < overlap_range_end:
                        next_values.append((overlap_range_start + mapping, overlap_range_end + mapping))
                        # add left outer overlap back in seeds
                        if seed_range_start < overlap_range_start:
                            seeds.append((seed_range_start, overlap_range_start))
                        # add right outer overlap back in seeds
                        if overlap_range_end < seed_range_end:
                            seeds.append((overlap_range_end, seed_range_end))
                        # doesn't need to continue since it can only exist one mapping per number
                        break
                # if no mapping found (exit for loop without breaking)
                else:
                    next_values.append((seed_range_start, seed_range_end))

            seeds = next_values

        res = min(seeds)[0]
        return res

    @staticmethod
    def unoptimized_part2(data: list[str]) -> int | str:
        index: int = 3
        seeds: list[int] = parse_ints(data[0])
        seed_to_soil: list[list[int]] = []
        seed_to_fertilizer: list[list[int]] = []
        fertilizer_to_water: list[list[int]] = []
        water_to_light: list[list[int]] = []
        light_to_temperature: list[list[int]] = []
        temperature_to_humidity: list[list[int]] = []
        humidity_to_location: list[list[int]] = []
        maps: list[list[list[int]]] = [seed_to_soil, seed_to_fertilizer, fertilizer_to_water, water_to_light,
                                       light_to_temperature, temperature_to_humidity, humidity_to_location]

        for _map in maps:
            for line in data[index::]:
                index += 1
                if line == '':
                    index += 1
                    break
                _map.append(parse_ints(line))

        res = math.inf
        for index in range(0, len(seeds), 2):
            seeds_range_start = seeds[index]
            seeds_range_length = seeds[index + 1]
            for seed in range(seeds_range_start, seeds_range_start + seeds_range_length):
                value = seed
                for _map in maps:
                    for dest, source, length in _map:
                        if source <= value < source + length:
                            value += dest - source
                            break

                res = min(res, value)

        return res


def main() -> None:
    directory = os.path.dirname(__file__)
    problem = Problem(directory)

    problem.exec_all(True)


if __name__ == "__main__":
    main()
