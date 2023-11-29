import os
import sys
from dataclasses import dataclass, field

from utils.exercise import Exercise


@dataclass
class Coord:
    x: int
    y: int


@dataclass
class Node:
    height: int
    coord: Coord
    min_steps: int = field(default=-1, init=False)
    links: list[Coord] = field(default_factory=list, init=False)


def is_in_grid(coord: Coord, length: int, height: int) -> bool:
    return (0 <= coord.x < length) and (0 <= coord.y < height)


def is_accessible_from(coord_to: Coord, coord_from: Coord, data: list[str]) -> bool:
    height_to = char_to_height(data[coord_to.y][coord_to.x])
    height_from = char_to_height(data[coord_from.y][coord_from.x])
    return height_to <= height_from + 1


def char_to_height(char: str) -> int:
    match char:
        case 'S':
            height = 0
        case 'E':
            height = 25
        case _:
            height = ord(char) - ord('a')
    return height


def get_node_at(coord: Coord, nodes: list[Node], length: int) -> Node:
    return nodes[coord.y * length + coord.x]


def visit(node: Node, nodes: list[Node], length: int, multiple_stating_point: bool) -> None:
    # 'a' node for part2
    if multiple_stating_point and node.height == 0:
        node.min_steps = 0
    current_steps = node.min_steps

    for link_coord in node.links:
        link_node = get_node_at(link_coord, nodes, length)
        # a shorter or equal path is already known
        if 0 <= link_node.min_steps <= current_steps + 1:
            continue
        else:
            link_node.min_steps = current_steps + 1
            visit(link_node, nodes, length, multiple_stating_point)


class Problem(Exercise):
    start_node = None
    end_node = None
    nodes: list[Node]
    grid_length: int
    grid_height: int

    def init_nodes(self, data: list[str]) -> None:
        self.nodes = []
        self.grid_length = len(data[0])
        self.grid_height = len(data)

        for y, line in enumerate(data):
            for x, char in enumerate(line):
                node_height = char_to_height(char)
                coord = Coord(x, y)
                node = Node(node_height, coord)

                if char == 'S':
                    self.start_node = node
                    self.start_node.min_steps = 0
                if char == 'E':
                    self.end_node = node

                neighbour = [(0, -1), (-1, 0), (1, 0), (0, 1)]
                for dx, dy in neighbour:
                    coord_neighbour = Coord(x + dx, y + dy)
                    if is_in_grid(coord_neighbour, self.grid_length, self.grid_height) and is_accessible_from(
                            coord_neighbour,
                            coord, data):
                        node.links.append(coord_neighbour)

                self.nodes.append(node)

    def resolve(self, data: list[str], multiple_starting_point: bool) -> int:
        self.init_nodes(data)

        # visit every reachable nodes from starting point
        visit(self.start_node, self.nodes, self.grid_length, multiple_starting_point)

        min_steps_to_end = self.end_node.min_steps
        return min_steps_to_end

    def part1(self, data: list[str]) -> int | str:
        min_steps_to_end = self.resolve(data, False)
        return min_steps_to_end

    def part2(self, data: list[str]) -> int | str:
        min_steps_to_end = self.resolve(data, True)
        return min_steps_to_end


def main() -> None:
    directory = os.path.dirname(__file__)
    problem = Problem(directory)

    sys.setrecursionlimit(2000)
    problem.exec_all(True)


if __name__ == "__main__":
    main()
