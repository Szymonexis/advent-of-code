choices = {
    'A': 0,
    'B': 1,
    'C': 2,
}

outcomes = {
    'X': 0,
    'Y': 3,
    'Z': 6,
}

offsets = {
    'X': -1,
    'Y': 0,
    'Z': 1,
}

score = 0
with open("2-2.txt") as file:
    for line in file.readlines():
        opponent, outcome = line.strip().split(' ')

        score += outcomes[outcome] + (choices[opponent] + offsets[outcome]) % 3 + 1

print(score)
