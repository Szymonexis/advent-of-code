from string import ascii_lowercase, ascii_uppercase


score = 0
with open('3-1.txt') as file:
    for line in file.readlines():
        letters = ascii_lowercase + ascii_uppercase
        stripped_line = line.strip()

        len_stripped = len(stripped_line)
        half_len = int(len_stripped / 2)

        compartment_one, compartment_two = stripped_line[0:half_len], stripped_line[half_len:len_stripped]

        flag = True
        for letter_one in compartment_one:
            for letter_two in compartment_two:
                if letter_one == letter_two and flag:
                    score += letters.find(letter_one) + 1
                    flag = False

print(score)
