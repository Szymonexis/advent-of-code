score = 0
with open("4-1.txt") as file:
    for line in file.readlines():
        line = line.strip()

        range_one, range_two = line.split(",")

        start_one, stop_one = 0, 0
        v_1, v_2 = range_one.split("-")
        start_one, stop_one = int(v_1), int(v_2)

        start_two, stop_two = 0, 0
        v_1, v_2 = range_two.split("-")
        start_two, stop_two = int(v_1), int(v_2)

        score += 1 if (start_one <= start_two and stop_one >=
                       stop_two) or (start_two <= start_one and stop_two >= stop_one) else 0

print(score)
