from text.texts import get_lines


def generate_forrest() -> list[list[int]]:
    forrest = []

    for line in get_lines(8):
        forrest.append([int(number) for number in line])

    return forrest


def main():
    forrest = generate_forrest()
    print(len(forrest), len(forrest[0]))
    pass


if __name__ == '__main__':
    main()
