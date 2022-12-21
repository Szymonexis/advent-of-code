def get_lines(day: int):
    with open(f'./text/{day}.txt') as file:
        return [line.strip() for line in file.readlines()]


if __name__ == '__main__':
    pass
