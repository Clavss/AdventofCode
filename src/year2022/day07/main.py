from __future__ import annotations

import math
import os
from dataclasses import dataclass, field

from utils.exercise import Exercise


@dataclass
class File:
    name: str
    size: int


@dataclass
class Folder:
    name: str
    parent: Folder | None
    folders: dict[str, Folder] = field(default_factory=dict, init=False)
    files: dict[str, File] = field(default_factory=dict, init=False)

    def add_folder(self, folder: Folder) -> None:
        self.folders[folder.name] = folder

    def add_file(self, file: File) -> None:
        self.files[file.name] = file

    def size(self) -> int:
        return sum([folder.size() for folder in self.folders.values()]) + sum(
            [file.size for file in self.files.values()])

    def process(self, line: str) -> None:
        start_line, name = line.split()
        if start_line == 'dir':
            self.add_folder(Folder(name, self))
        else:  # start_line is file size
            self.add_file(File(name, int(start_line)))


def total_folder_size(folder: Folder, limit_size: int) -> int:
    if folder is None:
        return 0

    size = folder.size()

    return (size if size <= limit_size else 0) + sum(
        [total_folder_size(f, limit_size) for f in folder.folders.values()])


def create_tree(data: list[str]) -> Folder:
    root = Folder('/', None)
    current_directory: Folder | None = None

    for line in data:
        if line.startswith('$ cd'):
            argument = line.removeprefix('$ cd ')
            # execute command
            if argument == '/':
                current_directory = root
            elif argument == '..':
                current_directory = current_directory.parent
            else:
                current_directory = current_directory.folders[argument]

        # not a command but a result of one (ls)
        elif not line.startswith('$'):
            current_directory.process(line)

    return root


def find_smallest_folder_size_above(folder: Folder, space_to_free: int) -> int:
    if folder is None:
        return 0

    size = folder.size()

    return min(size if size >= space_to_free else math.inf,
               min([find_smallest_folder_size_above(f, space_to_free) for f in folder.folders.values()],
                   default=math.inf))


class Problem(Exercise):
    def part1(self, data: list[str]) -> int | str:
        root = create_tree(data)
        return total_folder_size(root, 100_000)

    def part2(self, data: list[str]) -> int | str:
        root = create_tree(data)
        total_disk_space = 70_000_000
        needed_space = 30_000_000
        current_used_space = root.size()
        current_unused_space = total_disk_space - current_used_space
        space_to_free = needed_space - current_unused_space

        res = find_smallest_folder_size_above(root, space_to_free)
        return res


def main() -> None:
    directory = os.path.dirname(__file__)
    problem = Problem(directory)

    problem.exec_all()


if __name__ == "__main__":
    main()
