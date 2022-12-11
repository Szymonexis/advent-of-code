from string import ascii_letters

accumulator = []
score = 0
with open("3-2.txt") as file:
    for line_unstripped in file.readlines():
        line = line_unstripped.strip()
        accumulator.append(line)


        if len(accumulator) < 3:
            continue
        else:
            r_1, r_2, r_3 = accumulator

            flag = True
            for v_1 in r_1:
                for v_2 in r_2:
                    for v_3 in r_3:
                        if v_1 == v_2 == v_3 and flag:
                            score += ascii_letters.find(v_1) + 1
                            flag = False

                        if not flag:
                            break

            accumulator = []

print(score)
