from copy import copy
from enum import Enum
from text.texts import get_lines


class Direction(Enum):
    UP = 'U'
    DOWN = 'D'
    RIGHT = 'R'
    LEFT = 'L'


Operation = tuple[Direction, int]
Operations = list[Operation]
Position = tuple[int, int]
TailSpace = dict[str, bool]

MOVEMENTS: dict[Direction, Position] = {
    Direction.UP: (0, 1),
    Direction.DOWN: (0, -1),
    Direction.RIGHT: (1, 0),
    Direction.LEFT: (-1, 0),
}


# part one
def get_operations(lines: list[str]) -> Operations:
    operations: Operations = []

    for line in lines:
        direction, steps = line.split(' ')
        steps = int(steps)

        match direction:
            case 'U':
                operations.append((Direction.UP, steps))
            case 'D':
                operations.append((Direction.DOWN, steps))
            case 'R':
                operations.append((Direction.RIGHT, steps))
            case 'L':
                operations.append((Direction.LEFT, steps))

    return operations


def move_tail(current_head_position: Position,
              last_head_position: Position,
              tail_position: Position,
              tail_space: TailSpace) -> tuple[TailSpace, Position]:
    close_to_head = True
    tail_x, tail_y = tail_position
    head_x, head_y = current_head_position

    if abs(tail_x - head_x) > 1 or abs(tail_y - head_y) > 1:
        close_to_head = False

    if not close_to_head:
        # tail_offset shows where to put tail after head movement
        tail_offset = tuple(
            map(lambda i, j: i - j, last_head_position, current_head_position))

        tail_position = (
            current_head_position[0] + tail_offset[0], current_head_position[1] + tail_offset[1])

        tail_space[str(tail_position)] = True

    return tail_space, tail_position


def carry_out_moves(tail_space: TailSpace, operations: Operations) -> TailSpace:
    last_head_position = (None, None)
    # x - width, y - height  x  y
    current_head_position = (0, 0)
    tail_position = (0, 0)

    for (direction, steps) in operations:
        for _ in range(1, steps + 1):
            match direction:
                case Direction.UP:
                    last_head_position = current_head_position
                    current_head_position = (current_head_position[0],
                                             current_head_position[1] + 1)

                case Direction.DOWN:
                    last_head_position = current_head_position
                    current_head_position = (current_head_position[0],
                                             current_head_position[1] - 1)

                case Direction.RIGHT:
                    last_head_position = current_head_position
                    current_head_position = (current_head_position[0] + 1,
                                             current_head_position[1])

                case Direction.LEFT:
                    last_head_position = current_head_position
                    current_head_position = (current_head_position[0] - 1,
                                             current_head_position[1])

            tail_space, tail_position = move_tail(
                current_head_position, last_head_position, tail_position, tail_space)

    return tail_space


# part two
def carry_out_moves_two(rope: list[Position], operations: Operations) -> TailSpace:
    tail_space: TailSpace = {}

    for operation in operations:
        direction, steps = operation

        for _ in range(steps):
            # print_rope(rope)
            head_x, head_y = rope[0]
            movement_x, movement_y = MOVEMENTS[direction]
            rope[0] = (head_x + movement_x, head_y + movement_y)
            knots = rope[1:]

            for index in range(len(knots)):
                head = rope[index]
                if index != 0:
                    head = knots[index - 1]

                knot = knots[index]
                knots[index] = move_tail_two(head=head,
                                             tail=knot,
                                             direction=direction)

                if index == len(knots) - 1:
                    tail_space[str(knot)] = True

            rope = [rope[0]] + knots

    # print_rope(rope)
    return tail_space


def print_rope(rope: list[Position]) -> None:
    min_x = 0
    max_x = 0
    min_y = 0
    max_y = 0

    for position in rope:
        x, y = position

        min_x = min(min_x, x)
        min_y = min(min_y, y)

        max_x = max(max_x, x)
        max_y = max(max_y, y)

    positions_arr = [['.' for _ in range(min_x, max_x + 1)]
                     for _ in range(min_y, max_y + 1)]

    indexed_rope = list(map(
        lambda pos, i: (pos, i),
        rope,
        list(i for i in range(10))))

    for position, index in reversed(indexed_rope):
        x, y = position
        x = x - min_x
        y = y - min_y

        if index == 0:
            positions_arr[y][x] = 'H'
        else:
            positions_arr[y][x] = f'{index}'

    for _ in range(len(positions_arr[0]) + 2):
        print('.', end='')
    print()

    for line in reversed(positions_arr):
        print('.', end='')
        for char in line:
            print(char, end='')
        print('.')

    for _ in range(len(positions_arr[0]) + 2):
        print('.', end='')
    print()

    print()


# If the head is ever two steps directly up, down, left, or right from the tail,
# the tail must also move one step in that direction so it remains close enough.
# Otherwise, if the head and tail aren't touching and aren't in the
# same row or column, the tail always moves one step diagonally to keep up.
def move_tail_two(head: Position, tail: Position, direction: Direction) -> Position:
    if head_and_tail_are_touching(head, tail):
        return tail

    head_x, head_y = head
    tail_x, tail_y = tail

    off_x, off_y = (head_x - tail_x, head_y - tail_y)

    if head_is_two_steps_away(head, tail):
        if off_x >= 2:
            off_x = 1

        if off_x <= -2:
            off_x = -1

        if off_y >= 2:
            off_y = 1

        if off_y <= -2:
            off_y = -1

    return (tail_x + off_x, tail_y + off_y)


def head_and_tail_are_touching(head: Position, tail: Position) -> bool:
    head_x, head_y = head
    tail_x, tail_y = tail

    return not (abs(head_x - tail_x) > 1 or abs(head_y - tail_y) > 1)


def head_is_two_steps_away(head: Position, tail: Position) -> bool:
    head_x, head_y = head
    tail_x, tail_y = tail

    if abs(head_x - tail_x) >= 2:
        return True

    if abs(head_y - tail_y) >= 2:
        return True

    return False


def main():
    lines = get_lines(9)
    operations = get_operations(lines)

    # part one
    tail_space: TailSpace = {str((0, 0)): True}
    tail_space = carry_out_moves(tail_space, operations)

    print(f'part one answer: {len(list(tail_space.keys()))}')

    # part two
    rope = [(0, 0) for _ in range(10)]
    tail_space = carry_out_moves_two(rope, operations)
    print(f'part two answer: {len(list(tail_space.keys()))}')


if __name__ == '__main__':
    main()
