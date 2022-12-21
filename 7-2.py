from collections import defaultdict
from text.texts import get_lines


def get_sizes():
    lines = get_lines(7)
    # We can safely strip ls commands from the input
    lines = [entry for entry in lines if not entry == "$ ls"]
    filepath = []
    sizes = defaultdict(int)

    for entry in lines:
        if entry.startswith("$ cd"):
            match entry:
                case "$ cd /":
                    filepath.clear()
                    filepath.append("/")
                case "$ cd ..":
                    filepath.pop()
                case _:
                    dir = entry.split()[-1]
                    filepath.append(dir)
        else:
            # We have a listing of a file. Add the size to the current dir and all of its parent dirs.
            filesize = entry.split()[0]
            if filesize.isdigit():
                filesize = int(filesize)
                # Iterate through every dir in the full path to the file
                for i in range(len(filepath)):
                    dir = '/'.join(filepath[:i+1]).replace("//", "/")
                    sizes[dir] += filesize
    return sizes


def main():
    sizes = get_sizes()

    total_disk_space = 70000000
    needed_disk_space = 30000000
    space_to_free = sizes["/"] + needed_disk_space - total_disk_space
    dirs_above_threshold = {directory: size for (
        directory, size) in sizes.items() if size >= space_to_free}
    print(min(dirs_above_threshold.values()))


if __name__ == '__main__':
    main()
