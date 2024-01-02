from year2023.day10.main import get_ground, get_in_and_out_pos, find_start, find_loop


def test_ground():
    data = ['FF7FSF7F7F7F7F7F---7',
            'L|LJ||||||||||||F--J',
            'FL-7LJLJ||||||LJL-77',
            'F--JF--7||LJLJ7F7FJ-',
            'L---JF-JLJ.||-FJLJJ7',
            '|F|F-JF---7F7-L7L|7|',
            '|FFJF7L7F-JF7|JL---7',
            '7-L-JL7||F7|L7F-7F7|',
            'L.L7LFJ|||||FJL7||LJ',
            'L7JLJL-JLJLJL--JLJ.L']
    expected = ['OF7FSF7F7F7F7F7F---7',
                'O|LJ||||||||||||F--J',
                'OL-7LJLJ||||||LJL-7O',
                'F--JF--7||LJLJIF7FJO',
                'L---JF-JLJIIIIFJLJOO',
                'OOOF-JF---7IIIL7OOOO',
                'OOFJF7L7F-JF7IIL---7',
                'OOL-JL7||F7|L7F-7F7|',
                'OOOOOFJ|||||FJL7||LJ',
                'OOOOOL-JLJLJL--JLJOO']
    start_pos: complex = find_start(data)
    loop: set[complex] = set(find_loop(data, start_pos))
    in_pos, out_pos = get_in_and_out_pos(data, loop, start_pos)
    ground: list[str] = get_ground(data, loop, in_pos, out_pos)

    assert ground == expected
