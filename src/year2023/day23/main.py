from __future__ import annotations

import os
import re
from copy import copy, deepcopy
from dataclasses import dataclass, field

from utils.common import get_adjacent_positions, value_at, is_in_grid
from utils.exercise import Exercise

global_max: int = 0


def get_start_position(data: list[str]) -> complex:
    # start is the single path tile in the top row
    y: int = 0
    x: int = data[y].index('.')
    start_position: complex = complex(x, y)
    return start_position


def get_end_position(data: list[str]) -> complex:
    # end is the single path tile in the bottom row
    y: int = len(data) - 1
    x: int = data[y].index('.')
    end_position: complex = complex(x, y)
    return end_position


@dataclass()
class Save:
    current_position: complex
    path: set[complex] = field(default_factory=set)
    steps: int = 0


def find_longest_hike(data: list[str], start_position: complex, end_position: complex, part: int = 1) -> int:
    """Return the length of the longest path from start_position to end_position in data.

    This algorithm is inefficient as it computes every possible paths
    """
    seen: dict[complex, int] = {}
    to_visit: list[Save] = [Save(current_position=start_position)]

    while len(to_visit) > 0:
        save: Save = to_visit.pop()

        # part 1: already been there via a longer path, stop
        if part == 1 and seen.get(save.current_position, -1) >= save.steps:
            continue

        save.path.add(save.current_position)
        seen[save.current_position] = save.steps

        # reached the end, stop
        if save.current_position == end_position:
            print(save.steps)
            continue

        adjacent_positions: list[complex] = get_adjacent_positions(save.current_position)
        for position in adjacent_positions:
            # can't go out the grid or back on path
            if not is_in_grid(data, position) or position in save.path:
                continue

            char: str = value_at(data, position)

            # forest
            if char == '#':
                continue

            # for part 1:
            # right slope but not at our right
            # or down slope but not below
            if part == 1 and ((char == '>' and position.real <= save.current_position.real)
                              or (char == 'v' and position.imag <= save.current_position.imag)):
                continue

            to_visit.append(Save(position, copy(save.path), save.steps + 1))

    return seen.get(end_position)


def add_nodes(nodes: set[complex], data: list[str], pattern: str, reverse: bool = False) -> None:
    """Find intersections in data from pattern and add the corresponding position in nodes (inplace)."""
    for index, row in enumerate(data):
        intersections_indexes = [m.start() + 1 for m in re.finditer(pattern, row)]
        for intersections_index in intersections_indexes:
            if reverse:
                position: complex = complex(index, intersections_index)
            else:
                position: complex = complex(intersections_index, index)
            nodes.add(position)


def find_longest_graph_length(links_left: dict[complex, list[tuple[complex, int]]], from_position: complex,
                              end_position: complex, length: int) -> int:
    """Return the length of the longest path between from_position and end_position in the context graph links_left.

    Do a recursive Depth First Search on all possible paths.
    """
    possibilities: list[tuple[complex, int]] = links_left.get(from_position)

    # try to reach the end directly from position.
    # because the end node only has one link, if we don't take this link to reach the end when it's possible,
    # it will be impossible to do so later as we will have to visit the node a second time.
    try:
        index: int = [p[0] for p in possibilities].index(end_position)
    except ValueError:
        pass
    else:
        length_to_end: int = possibilities[index][1]
        return length + length_to_end

    lengths_from_position_to_end: list[int] = []
    # visit each connected node
    for possibility in possibilities:
        to_pos, steps = possibility

        # node already visited
        if to_pos not in links_left.keys():
            continue

        # TODO: have a way to know if we are going towards the start or the end
        # heuristic: if we are on an outer edge of the graph,
        # continuing towards the start will make the end unreachable as it will form a loop.
        # every inner edge has 4 links

        new_links_left: dict[complex, list[tuple[complex, int]]] = deepcopy(links_left)
        # mark this node as visited by deleting it from the remaining possibilities
        del new_links_left[from_position]
        new_length: int = length + steps

        length_from_position_to_end: int = find_longest_graph_length(new_links_left, to_pos, end_position, new_length)

        # don't count dead end paths
        if length_from_position_to_end != -1:
            lengths_from_position_to_end.append(length_from_position_to_end)

    # dead end
    if not lengths_from_position_to_end:
        return -1

    local_max = max(lengths_from_position_to_end)

    global global_max
    if local_max > global_max:
        global_max = local_max
        print('new max', global_max)

    return local_max


def efficient_longest_path_length(data: list[str], start_position: complex, end_position: complex) -> int:
    """Return the length of the longest path from start_position to end_position in data.

    Using the fact that every path in the maze is always 1 tile wide and intersections are between arrows,
    we can create a graph from it.
    """

    # parsing
    nodes: set[complex] = {start_position, end_position}
    add_nodes(nodes, data, '>.>')
    add_nodes(nodes, [''.join(el) for el in zip(*data)], 'v.v', reverse=True)

    # for each node, visit every direction until finding another node
    # create a link containing every 2 connected nodes and the distance between them
    links: dict[complex, list[tuple[complex, int]]] = {}
    for node in nodes:
        # [(position, length)]
        to_visit: list[tuple[complex, int]] = [(node, 0)]
        seen: set[complex] = set()

        while len(to_visit) > 0:
            current_position, length = to_visit.pop()

            if current_position in seen:
                continue

            seen.add(current_position)

            # other node found, create a link if not already existing
            if current_position != node and current_position in nodes:
                node_links = links.get(node, [])
                if current_position not in node_links:
                    links[node] = node_links + [(current_position, length)]
                continue

            adjacent_positions: list[complex] = get_adjacent_positions(current_position)
            for position in adjacent_positions:
                # can't go out the grid or in a tree
                if not is_in_grid(data, position) or value_at(data, position) == '#':
                    continue

                to_visit.append((position, length + 1))

    longest_graph_length: int = find_longest_graph_length(deepcopy(links), start_position, end_position, 0)
    return longest_graph_length


class Problem(Exercise):

    def part1(self, data: list[str]) -> int | str:
        start_position: complex = get_start_position(data)
        end_position: complex = get_end_position(data)

        longest_hike: int = find_longest_hike(data, start_position, end_position)
        return longest_hike

    def part2(self, data: list[str]) -> int | str:
        start_position: complex = get_start_position(data)
        end_position: complex = get_end_position(data)

        # should work but way too long to finish:
        # longest_hike: int = find_longest_hike(data, start_position, end_position, part=2)

        longest_hike: int = efficient_longest_path_length(data, start_position, end_position)
        return longest_hike


def main() -> None:
    directory = os.path.dirname(__file__)
    problem = Problem(directory)

    problem.exec_part(2, True)


if __name__ == "__main__":
    main()
