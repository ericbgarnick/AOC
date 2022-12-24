"""
Part 1 answer: 2031851
Part 2 answer: 2568781
"""
from enum import Enum
from typing import TextIO, Type, Optional

from y2022.python.shared import get_data_file_path

FILESYSTEM_SIZE = 70000000
MAX_DIR_SIZE = 100000
COMMAND_PROMPT = "$"
ROOT_DIR_PATH = "/"
ROOT_DIR_NAME = ""
PARENT_DIR = ".."


class NodeType(Enum):
    file = "file"
    directory = "directory"

class Node:
    def __init__(
        self, name: str,
        node_type: NodeType,
        parent: Optional['Node'] = None,
        size: int = 0,
    ):
        self.name = name
        self.parent = parent
        self._node_type = node_type
        self._contents: set['Node'] = set()
        self._size = size

    def __str__(self) -> str:
        suffix = "/" if self._node_type == NodeType.directory else f" (self._size)"
        return self.name + suffix

    @property
    def size(self) -> int:
        if self._node_type == NodeType.file:
            return self._size
        return sum(c.size for c in self._contents)

    @property
    def contents(self) -> set[str] | None:
        if self._node_type == NodeType.file:
            return None
        return {c.name for c in self._contents}

    @property
    def path(self) -> str | None:
        if self._node_type == NodeType.file:
            return None
        if self.parent:
            path = self.parent.path
        else:
            path = ""
        return path + f"{self.name}/"

    def add_contents(self, file_or_dir: 'Node'):
        self._contents.add(file_or_dir)


def parse_terminal_output(buffer: TextIO) -> dict[str, Node]:
    """
    Return a mapping of path/to/directory/ mapped to the Node for that directory.
    """
    cur_dir = Node(ROOT_DIR_NAME, NodeType.directory)
    dir_map = {cur_dir.path: cur_dir}
    for line in buffer:
        if line[0] == COMMAND_PROMPT:
            command = line.strip().split()[1:]
            if command[0] == "cd":
                cur_dir = change_directory(command[1], cur_dir, dir_map)
            else:
                # Move to the next line after 'ls'
                continue
        else:
            record_object(line.strip(), cur_dir, dir_map)
    return dir_map


def change_directory(dir_name: str, cur_dir: Node, dir_map: dict[str, Node]) -> Node:
    if dir_name == PARENT_DIR:
        cur_dir = cur_dir.parent
    elif dir_name == ROOT_DIR_PATH:
        cur_dir = dir_map[ROOT_DIR_PATH]
    else:
        cur_path = cur_dir.path
        cur_dir = dir_map[cur_path + f"{dir_name}/"]
    return cur_dir


def record_object(output_line: str, cur_dir: Node, dir_map: dict[str, Node]):
    """
    Create a new Node for output_line.

    For files, add the new Node to cur_dir contents.
    For directories, add the new Node to dir_map keyed by its absolute path.
    """
    dir_or_size, node_name = output_line.split()
    if dir_or_size == "dir":
        new_node = Node(node_name, NodeType.directory, parent=cur_dir)
        dir_map[new_node.path] = new_node
    else:
        new_node = Node(node_name, NodeType.file, size=int(dir_or_size))
    if node_name not in cur_dir.contents:
        cur_dir.add_contents(new_node)

def main():
    with open(get_data_file_path(__file__.split("/")[-1]), "r") as f_in:
        dir_map = parse_terminal_output(f_in)

    # PART 1
    total_size = sum(d.size for d in dir_map.values() if d.size <= MAX_DIR_SIZE)
    print("PART 1:", total_size)

    # PART 2
    required_space = 30000000
    unused_space = FILESYSTEM_SIZE - dir_map[ROOT_DIR_PATH].size
    min_del_size = required_space - unused_space
    target_dir_size = min(d.size for d in dir_map.values() if d.size >= min_del_size)
    print("PART 2:", target_dir_size)


if __name__ == "__main__":
    main()
