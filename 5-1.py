import re

CratesColumn = list[str]
Move = tuple[int, int, int]
Moves = list[Move]
Crates = list[CratesColumn]


def get_file_contents() -> tuple[Crates, Moves]:
    crates: Crates = [[] for _ in range(9)]
    moves: Moves = []
    is_after_number_row = False

    with open("5-1.txt") as file:
        for line in file.readlines():
            index = 0
            line = line.strip()

            if line != "" and line[0] == "1":
                is_after_number_row = True
                continue

            # get crates
            if not is_after_number_row:
                for sub in re.split("[ ]{3} ", line):
                    sub = sub.strip()

                    if sub == "":
                        index += 1
                    else:
                        for element in sub.split(" "):
                            if element != "":
                                crates[index].append(element)
                            index += 1
                        index += 1

            # get moves
            index = 0
            if is_after_number_row and line != "":
                moves_line = []
                for char in re.split("[move | from | to ]", line):
                    if char != "":
                        moves_line.append(int(char))
                moves.append((moves_line[0], moves_line[1], moves_line[2]))

    for crate_column in crates:
        crate_column.reverse()

    return (crates, moves)


def move_crates(move: Move, crates: Crates):
    for _ in range(move[0]):
        crates[move[2] - 1].append(crates[move[1] - 1].pop())


def print_crates(crates: Crates):
    index = 1
    for crate_column in crates:
        print(f"{index} {crate_column}")
        index += 1


def print_top_crates(crates: Crates):
    for crate_column in crates:
        crate_column.reverse()

    print_str = ""
    result = ""
    for index, crate_cloumn in enumerate(crates):
        print_str += f"{crate_cloumn[0]}"
        result += f"{crate_cloumn[0][1:2]}"
        if index != len(crates) - 1:
            print_str += ", "

    print(f"Top crates are: {print_str}")
    print(f"{result}")


crates, moves = get_file_contents()

print_crates(crates)

for move in moves:
    move_crates(move, crates)

print_top_crates(crates)
