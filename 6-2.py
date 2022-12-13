with open("6-1.txt") as file:
    line = file.readline().strip()

    start = 14
    potentiall_marker = line[0:start]
    index = start

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
        potentiall_marker = line[index - start:index]
    
    print(index - 1)


