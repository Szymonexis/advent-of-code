from enum import Enum
from text.texts import get_lines


class Operation(Enum):
    NOOP = 'noop'
    ADDX = 'addx'


Lines = list[str]
Cycles = int
X_Value = int | None
Operations = list[tuple[Operation, Cycles, X_Value]]


def get_operations(lines: Lines) -> Operations:
    operations: Operations = []

    for line in lines:
        match line:
            case r"noop":
                operations.append((Operation.NOOP, 1, None))
            case _:
                value = int(line.split(' ')[1])
                operations.append((Operation.ADDX, 2, value))

    return operations


def carry_out_instructions(operations: Operations, cycles_to_sum: list[int]) -> int:
    global_cycle = 0
    x_registry = 1

    operation_index = 0
    operation, cycle, value = operations[operation_index]

    sum_of_signal_strengths = 0

    while True:
        try:
            global_cycle += 1
            operation, cycle, value = operations[operation_index]

            if cycle == 0:
                if operation == Operation.ADDX:
                    x_registry += value

                operation_index += 1
                operation, cycle, value = operations[operation_index]

            # print(f'global_cycle: {global_cycle}')
            # print(f'x_registry: {x_registry}')

            if global_cycle in cycles_to_sum:
                signal_strength = global_cycle * x_registry
                sum_of_signal_strengths += signal_strength

                # print(f'signal_strength: {signal_strength}')

            # print('-----------------\n')

            operations[operation_index] = (operation, cycle - 1, value)

        except IndexError:
            break

    return sum_of_signal_strengths


# part two
def recreate_crt_image(operations: Operations) -> None:
    crt = create_crt()
    sprite = create_sprite()

    global_cycle = 0
    x_registry = 1

    operation_index = 0
    operation, cycle, value = operations[operation_index]

    while True:
        try:
            crt_cycle = global_cycle
            global_cycle += 1
            operation, cycle, value = operations[operation_index]

            if cycle == 0:
                if operation == Operation.ADDX:
                    x_registry += value
                    sprite = ['.' for _ in range(40)]

                    if 0 <= x_registry < 40:
                        sprite[x_registry] = '#'

                    if 0 <= (x_registry + 1) < 40:
                        sprite[x_registry + 1] = '#'

                    if 0 <= (x_registry - 1) < 40:
                        sprite[x_registry - 1] = '#'

                operation_index += 1
                operation, cycle, value = operations[operation_index]

            # print(f'global_cycle: {global_cycle}')
            # print(f'x_registry: {x_registry}')
            # print('sprite:')
            # print_sprite(sprite)
            # print('crt:')
            # print_crt(crt)
            # print('-----------------\n')

            operations[operation_index] = (operation, cycle - 1, value)

            crt[crt_cycle // 40][crt_cycle % 40] = sprite[crt_cycle % 40]

        except IndexError:
            break

    return crt


def print_crt(crt) -> None:
    for line in crt:
        for char in line:
            print(char, end='')
        print()


def print_sprite(sprite) -> None:
    for char in sprite:
        print(char, end='')
    print()


def create_crt() -> list[list[str]]:
    crt = [['.' for _ in range(40)] for _ in range(6)]
    return crt


def create_sprite() -> list[str]:
    sprite = []

    for index in range(40):
        if index < 3:
            sprite.append('#')
        else:
            sprite.append('.')

    return sprite


def main():
    lines = get_lines(10)

    operations = get_operations(lines)
    cycles_to_sum = [20, 60, 100, 140, 180, 220]

    # part one
    sum_of_signal_strengths = carry_out_instructions(operations, cycles_to_sum)
    print(f'sum_of_signal_strengths: {sum_of_signal_strengths}')

    # part two
    operations = get_operations(lines)
    crt = recreate_crt_image(operations)
    print('crt:')
    print_crt(crt)


if __name__ == '__main__':
    main()
