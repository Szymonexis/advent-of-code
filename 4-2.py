score = 0
with open("4-2.txt") as file:
    for line in file.readlines():
        line = line.strip()

        ranges = line.split(",")
        vals_one = [int(x) for x in ranges[0].split("-")]
        vals_two = [int(x) for x in ranges[1].split("-")]

        end = max([vals_one[1], vals_two[1]])
        range_space = [None for _ in range(end + 1)]

        for index in range(vals_one[0], vals_one[1] + 1):
            range_space[index] = 0

        flag = False
        for index in range(vals_two[0], vals_two[1] + 1):
            if range_space[index] is not None:
                flag = True
                break

        if flag:
            score += 1

print(score)