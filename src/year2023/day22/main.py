from __future__ import annotations

import math
import os
from dataclasses import dataclass, field
from functools import cache

from utils.exercise import Exercise


@dataclass
class Point2d:
    x: int
    y: int


@dataclass(unsafe_hash=True)
class Point3d(Point2d):
    z: int


@cache
def blocks_between(start_pos: tuple[int, int, int], end_pos: tuple[int, int, int]) -> list[tuple[int, int, int]]:
    blocks: list[tuple[int, int, int]] = []
    for x in range(start_pos[0], end_pos[0] + 1):
        for y in range(start_pos[1], end_pos[1] + 1):
            for z in range(start_pos[2], end_pos[2] + 1):
                pos: tuple[int, int, int] = (x, y, z)
                blocks.append(pos)
    return blocks


@dataclass(unsafe_hash=True)
class Brick:
    name: str
    start_pos: Point3d
    end_pos: Point3d

    def update(self, x: int = 0, y: int = 0, z: int = 0) -> None:
        for pos in [self.start_pos, self.end_pos]:
            pos.x += x
            pos.y += y
            pos.z += z

    def get_blocks(self) -> list[tuple[int, int, int]]:
        blocks: list[tuple[int, int, int]] = blocks_between((self.start_pos.x, self.start_pos.y, self.start_pos.z), (
            self.end_pos.x, self.end_pos.y, self.end_pos.z))
        return blocks


@dataclass
class Map3d:
    grid: dict[tuple[int, int, int], Brick] = field(default_factory=dict)

    def add(self, brick: Brick) -> None:
        blocks: list[tuple[int, int, int]] = brick.get_blocks()
        for block in blocks:
            self.grid[block] = brick

    def get_max_space_under_brick(self, brick: Brick) -> int:
        # if the brick is vertical, only look under the lowest block (start_pos)
        if brick.start_pos.z != brick.end_pos.z:
            return self.get_max_space_under_block((brick.start_pos.x, brick.start_pos.y, brick.start_pos.z))
        return min([self.get_max_space_under_block(block) for block in brick.get_blocks()])

    def get_max_space_under_block(self, block: tuple[int, int, int]) -> int:
        block_x, block_y, block_z = block
        for z in range(block_z - 1, 0, -1):
            if (block_x, block_y, z) in self.grid.keys():
                return block_z - z - 1
        # there is nothing under but the floor
        return block_z - 1

    def update_brick(self, brick: Brick, x: int = 0, y: int = 0, z: int = 0) -> None:
        for block in brick.get_blocks():
            pos_before: tuple[int, int, int] = block
            pos_after: tuple[int, int, int] = (pos_before[0] + x, pos_before[1] + y, pos_before[2] + z)

            self.remove_block(pos_before)
            self.add_block(pos_after, brick)

    def add_block(self, block: tuple[int, int, int], brick: Brick) -> None:
        self.grid[block] = brick

    def remove_block(self, block: tuple[int, int, int]) -> None:
        del self.grid[block]

    def get_bricks_above(self, brick: Brick) -> list[Brick]:
        return self.get_bricks_at_z(brick, 1)

    def get_bricks_under(self, brick: Brick) -> list[Brick]:
        return self.get_bricks_at_z(brick, -1)

    def get_bricks_at_z(self, brick: Brick, delta_z: int) -> list[Brick]:
        bricks: list[Brick] = []
        for x, y, z in brick.get_blocks():
            adjacent_brick: Brick = self.grid.get((x, y, z + delta_z), None)
            if adjacent_brick not in [None, brick, *bricks]:
                bricks.append(adjacent_brick)

        return bricks


def get_name(index) -> str:
    letters: str = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    res: str = letters[index % len(letters)]
    return res


def create_map(bricks: list[Brick]) -> Map3d:
    map3d: Map3d = Map3d()

    for brick in bricks:
        map3d.add(brick)

    return map3d


def print_map(map3d: Map3d, axis: str) -> None:
    min_x: int | float = math.inf
    min_y: int | float = math.inf
    min_z: int | float = math.inf
    max_x: int = 0
    max_y: int = 0
    max_z: int = 0
    for block in map3d.grid.keys():
        x, y, z = block
        min_x = min(min_x, x)
        min_y = min(min_y, y)
        min_z = min(min_z, z)
        max_x = max(max_x, x)
        max_y = max(max_y, y)
        max_z = max(max_z, z)

    min_axis1: int = [min_y, min_x][axis == 'x']
    max_axis1: int = [max_y, max_x][axis == 'x']
    for z in range(max_z, min_z - 1, -1):
        for axis1 in range(min_axis1, max_axis1 + 1):
            char: str = '.'
            if axis == 'x':
                for b in range(min_y, max_y + 1):
                    if (axis1, b, z) in map3d.grid.keys():
                        char = map3d.grid.get((axis1, b, z)).name
                        break
            else:
                for a in range(max_x, 0, -1):
                    if (a, axis1, z) in map3d.grid.keys():
                        char = map3d.grid.get((a, axis1, z)).name
                        break

            print(char, end='')
        print()


def fall_downward(bricks: list[Brick], map3d: Map3d) -> None:
    """Lower the z coordinate of each brick as much as possible."""
    bricks.sort(key=lambda el: el.start_pos.z)
    for brick in bricks:
        # already on the floor
        if brick.start_pos.z == 1:
            continue

        max_space_under_brick: int = map3d.get_max_space_under_brick(brick)

        map3d.update_brick(brick, z=-max_space_under_brick)
        brick.update(z=-max_space_under_brick)


def nb_disintegrable_bricks(map3d: Map3d, bricks: list[Brick]) -> int:
    count: int = 0
    for brick in bricks:
        bricks_above: list[Brick] = map3d.get_bricks_above(brick)
        # all bricks supported by brick (directly above it)
        # should have at least 2 (one other than brick) bricks supporting it (directly under it)
        if all([len(map3d.get_bricks_under(brick)) > 1 for brick in bricks_above]):
            count += 1
    return count


def get_bricks_only_supported_by(bricks: set[Brick], map3d: Map3d) -> set[Brick]:
    """Return the set of bricks only supported by given bricks."""
    bricks_above: set[Brick] = set()
    for brick in bricks:
        for brick_above in map3d.get_bricks_above(brick):
            bricks_above.add(brick_above)
    return set(filter(lambda el: set(map3d.get_bricks_under(el)).issubset(bricks), bricks_above))


def nb_falling_bricks_removing(brick: Brick, map3d: Map3d) -> int:
    seen: set[Brick] = {brick}
    count: int = -1

    while len(seen) > 0:
        count += len(seen)
        seen = get_bricks_only_supported_by(seen, map3d)

    # print(brick, count)
    return count


class Problem(Exercise):

    def part1(self, data: list[str]) -> int | str:
        bricks: list[Brick] = []

        for index, line in enumerate(data):
            split: list[str] = line.split('~')

            name: str = get_name(index)
            start_pos: Point3d = Point3d(*map(int, split[0].split(',')))
            end_pos: Point3d = Point3d(*map(int, split[1].split(',')))

            block: Brick = Brick(name, start_pos, end_pos)
            bricks.append(block)

        map3d: Map3d = create_map(bricks)

        fall_downward(bricks, map3d)

        # print_map(map3d, 'x')
        # print_map(map3d, 'y')

        count: int = nb_disintegrable_bricks(map3d, bricks)
        return count

    def part2(self, data: list[str]) -> int | str:
        bricks: list[Brick] = []

        for index, line in enumerate(data):
            split: list[str] = line.split('~')

            name: str = get_name(index)
            start_pos: Point3d = Point3d(*map(int, split[0].split(',')))
            end_pos: Point3d = Point3d(*map(int, split[1].split(',')))

            block: Brick = Brick(name, start_pos, end_pos)
            bricks.append(block)

        map3d: Map3d = create_map(bricks)

        fall_downward(bricks, map3d)

        count: int = sum([nb_falling_bricks_removing(brick, map3d) for brick in bricks])
        return count


def main() -> None:
    directory = os.path.dirname(__file__)
    problem = Problem(directory)

    problem.exec_all(True)


if __name__ == "__main__":
    main()

# 42671
# 43890
# ?
