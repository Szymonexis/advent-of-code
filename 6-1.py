from text.texts import get_lines

for line in get_lines(6):
    potentiall_marker = line[0:4]
    index = 4

    is_marker = False
    while not is_marker:
        letters: dict[str, int] = {}

        for letter in potentiall_marker:
            if letters.get(letter) is None:
                letters[letter] = 0
            else:
                letters[letter] += 1

        temp_is_marker = True
        for letter in letters:
            if letters[letter] > 0:
                temp_is_marker = False

        is_marker = temp_is_marker
        index += 1
        potentiall_marker = line[index - 4:index]
    
    print(index - 1)


