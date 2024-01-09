from typing import TypeVar, Tuple, Any

T = TypeVar('T')


def value_at(data: list[T], position: complex) -> T:
    x: int = int(position.real)
    y: int = int(position.imag)
    return data[y][x]


def is_in_grid(grid: list[str], position: complex) -> bool:
    x: int = int(position.real)
    y: int = int(position.imag)
    length: int = len(grid[0])
    height: int = len(grid)
    return 0 <= x < length and 0 <= y < height


def get_adjacent_positions(position: complex) -> list[complex]:
    adjacent_positions: list[complex] = []
    delta_positions: list[complex] = [0 - 1j, 0 + 1j, -1 + 0j, 1 + 0j]
    for delta_position in delta_positions:
        adjacent_position = position + delta_position
        adjacent_positions.append(adjacent_position)
    return adjacent_positions


def replace_str_at(text: str, index: int, replacement: str) -> str:
    return f'{text[:index]}{replacement}{text[index + 1:]}'


def replace_tuple_at(_tuple: tuple[T, ...], index: int, replacement: T) -> tuple[Any, ...]:
    return *_tuple[:index], replacement, *_tuple[index + 1:]
