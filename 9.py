from enum import Enum
from text.texts import get_lines


class Direction(Enum):
    UP = 'U'
    DOWN = 'D'
    RIGHT = 'R'
    LEFT = 'L'


Operations = list[tuple[Direction, int]]
Position = tuple[int, int]
TailSpace = dict[str, bool]
TailSegmentPositions = tuple[Position, Position]


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


# TODO: something wrong, fix it :( 
def carry_out_moves_long_tail(
        tail_space: TailSpace,
        operations: Operations,
        tail_segments_positions: list[TailSegmentPositions]
) -> TailSpace:
    last_head_position = (None, None)
    # x - width, y - height  x  y
    current_head_position = (0, 0)

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

        for index, tail_segment_positions in enumerate(tail_segments_positions):
            last_tail_segment_position = tail_segment_positions[1]
            
            if index == 0:
                current_tail_segment_position = move_tail(
                    current_head_position, last_head_position, last_tail_segment_position, tail_space)[1]
            elif index == len(tail_segments_positions) - 1:
                tail_space, current_tail_segment_position = move_tail(
                    tail_segments_positions[index - 1][1], tail_segments_positions[index - 1][0], last_tail_segment_position, tail_space)
            else:
                current_tail_segment_position = move_tail(
                    tail_segments_positions[index - 1][1], tail_segments_positions[index - 1][0], last_tail_segment_position, tail_space)[1]

            tail_segments_positions[index] = (last_tail_segment_position, current_tail_segment_position)

    return tail_space


def main():
    # part one
    lines = get_lines(9)
    operations = get_operations(lines=lines)

    tail_space: TailSpace = {str((0, 0)): True}
    tail_space = carry_out_moves(tail_space, operations)

    print(f'part one answer: {len(list(tail_space.keys()))}')

    # part two
    tail_space: TailSpace = {str((0, 0)): True}
    tail_segments_positions: list[TailSegmentPositions] = [
        ((0, 0), (0, 0)) for _ in range(9)]
    tail_space = carry_out_moves_long_tail(
        tail_space, operations, tail_segments_positions)

    print(f'part one answer: {len(list(tail_space.keys()))}')


if __name__ == '__main__':
    main()
