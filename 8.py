from enum import Enum
from text.texts import get_lines


class Direction(Enum):
    Up = 'up'
    Down = 'down'
    Right = 'right'
    Left = 'left'


def generate_forest() -> list[list[int]]:
    forrest = []

    for line in get_lines(8):
        forrest.append([int(number) for number in line])

    return forrest


def is_highest(forest_slice: list[int], provided_tree: int) -> bool:
    for tree in forest_slice:
        if tree >= provided_tree:
            return False
    return True


def calculate_score(forest_slice: list[int], provided_tree) -> int:
    for index, tree in enumerate(forest_slice):
        if tree >= provided_tree:
            return len(forest_slice[0:index + 1])

    return len(forest_slice)


def get_slice(forest: list[list[int]], coords: tuple[int, int], direction: Direction) -> bool:
    forest_slice = []
    y, x = coords

    match direction:
        case Direction.Up:
            forest_slice = list(reversed([row[x] for row in forest[0:y]]))
        case Direction.Down:
            forest_slice = [row[x] for row in forest[y + 1:len(forest)]]
        case Direction.Right:
            forest_slice = [tree for tree in forest[y][x + 1:len(forest[0])]]
        case Direction.Left:
            forest_slice = list(reversed([tree for tree in forest[y][0:x]]))

    return forest_slice


def main():
    forest = generate_forest()

    # part one
    visible_trees = []
    for y, row in enumerate(forest):
        for x, tree in enumerate(row):
            if is_highest(get_slice(forest, (y, x), Direction.Up), tree):
                visible_trees.append(tree)
                continue

            if is_highest(get_slice(forest, (y, x), Direction.Down), tree):
                visible_trees.append(tree)
                continue

            if is_highest(get_slice(forest, (y, x), Direction.Right), tree):
                visible_trees.append(tree)
                continue

            if is_highest(get_slice(forest, (y, x), Direction.Left), tree):
                visible_trees.append(tree)
                continue

    print(f'len(visible_trees): {len(visible_trees)}')

    # part two
    max_score = 0
    for y, row in enumerate(forest):
        for x, tree in enumerate(row):
            score = 1
            for direction in Direction:
                score *= calculate_score(get_slice(forest,
                                         (y, x), direction), tree)
            max_score = max(max_score, score)

    print(f'max_score: {max_score}')


if __name__ == '__main__':
    main()
