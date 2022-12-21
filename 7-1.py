from __future__ import annotations
from enum import Enum
from typing import Type
import re
from dataclasses import dataclass


@dataclass
# noinspection PyPep8Naming
class regex_in:
    string: str

    def __eq__(self, other: str | re.Pattern):
        if isinstance(other, str):
            other = re.compile(other)
        assert isinstance(other, re.Pattern)
        # TODO extend for search and match variants
        return other.fullmatch(self.string) is not None


class NodeType(Enum):
    FILE = 0
    DIR = 1


class Node:
    def __init__(self, name, node_type=NodeType.DIR, size=0):
        self.name: str = name
        self.type: NodeType = node_type
        self.size: int = size
        self.children: list[Node] = []
        self.parent: Node = None

    def add_child(self, child: Node):
        if child not in self.children:
            self.children.append(child)

    def print(self, level=0):
        prefix = "|\t"
        print(f'{prefix * level}{self}')

        for child in self.children:
            child.print(level + 1)
        pass

    def __str__(self) -> str:
        return f'DIR: {self.name}({self.size})' if self.type == NodeType.DIR else f'FILE: {self.name}({self.size})'

    def __repr__(self) -> str:
        return f'DIR: {self.name}({self.size})' if self.type == NodeType.DIR else f'FILE: {self.name}({self.size})'

    def __hash__(self) -> int:
        return self.name.__hash__()

    def __eq__(self, other: Node) -> bool:
        return self.name == other.name


def parse_input() -> Node:
    root_node: Node = None

    with open("7-1.txt") as file:
        for line in file.readlines():
            line = line.strip()

            match regex_in(line):
                case r'^\$ cd .+$':
                    go_to_name = line[5:]

                    match go_to_name:
                        case '..':
                            current_node = current_node.parent
                        case '/':
                            root_node = Node('/')
                            current_node = root_node
                        case _:
                            has_child = False
                            for child in current_node.children:
                                if child.name == go_to_name:
                                    current_node = child
                                    has_child = True
                                    break

                            if has_child == False:
                                new_node = Node(go_to_name)
                                new_node.parent = current_node
                                current_node.children.append(new_node)
                                current_node = new_node

                case r'^\$ ls$':
                    pass

                case r'^dir .+$':
                    new_node = Node(line[5:])
                    new_node.parent = current_node
                    current_node.children.append(new_node)

                case r'^[0-9]+ .+$':
                    size_str, name = line.split(" ")
                    new_node = Node(name, NodeType.FILE, int(size_str))
                    new_node.parent = current_node
                    current_node.children.append(new_node)

    return root_node


def collect_last_dirs(node: Node) -> list[Node]:
    # dir is last if has no children or its children are only files

    last_dirs = []

    for child in node.children:
        if child.type == NodeType.FILE:
            continue

        len_children = len(child.children)

        only_files = True
        for sub_child in child.children:
            if sub_child.type == NodeType.DIR:
                only_files = False
                break

        if len_children == 0 or only_files:
            last_dirs.append(child)
        else:
            last_dirs += collect_last_dirs(child)

    return last_dirs


def assign_dir_sizes(last_dirs: list[Node]):
    next_dirs = last_dirs

    while len(next_dirs) != 0:
        for dir in next_dirs:
            size = 0
            for child in dir.children:
                size += child.size

            dir.size += size

        temp_next_dirs = []
        for dir in next_dirs:
            if dir.parent is not None:
                temp_next_dirs.append(dir.parent)

        next_dirs = list(set(temp_next_dirs))


def collect_dirs_of_max_size(node: Node, max_size=100000) -> list[Node]:
    dirs = []

    for child in node.children:
        if child.type == NodeType.FILE:
            continue

        if child.size <= max_size:
            dirs.append(child)
        else:
            dirs += collect_dirs_of_max_size(child)

    return dirs


root_node = parse_input()
root_node.print()

assign_dir_sizes(collect_last_dirs(root_node))
root_node.print()

max_size_dirs = collect_dirs_of_max_size(root_node)
print(max_size_dirs)

print(sum([node.size for node in max_size_dirs]))
