import pytest
from y2022.python.day07.day07 import Node, NodeType, change_directory


def test_node_size():
    # GIVEN
    root_dir = Node("", NodeType.directory)
    file_1 = Node("file_1", NodeType.file, size=11)
    subdir = Node("subdir", NodeType.directory, parent=root_dir)
    file_2 = Node("file_2", NodeType.file, size=22)
    file_3 = Node("file_3", NodeType.file, size=33)

    root_dir.add_contents(file_1)
    root_dir.add_contents(subdir)
    subdir.add_contents(file_2)
    subdir.add_contents(file_3)

    # THEN
    assert file_1.size == 11
    assert file_2.size == 22
    assert file_3.size == 33
    assert subdir.size == 55
    assert root_dir.size == 66


def test_node_path():
    # GIVEN
    root_dir = Node("", NodeType.directory)
    file_1 = Node("file_1", NodeType.file, size=11)
    subdir = Node("subdir", NodeType.directory, parent=root_dir)
    file_2 = Node("file_2", NodeType.file, size=22)
    file_3 = Node("file_3", NodeType.file, size=33)

    root_dir.add_contents(file_1)
    root_dir.add_contents(subdir)
    subdir.add_contents(file_2)
    subdir.add_contents(file_3)

    # THEN
    assert file_1.path is None
    assert file_2.path is None
    assert file_3.path is None
    assert subdir.path == "/subdir/"
    assert root_dir.path == "/"


@pytest.mark.parametrize(
    "dest_dir_name,cur_dir_path,expected_dir_path",
    [
        pytest.param("/", "/subdir/subsubdir/", "/", id="jump to root"),
        pytest.param(
            "subsubdir",
            "/subdir/",
            "/subdir/subsubdir/",
            id="descend into subdirectory",
        ),
        pytest.param(
            "..", "/subdir/subsubdir/", "/subdir/", id="ascend to parent directory"
        ),
    ],
)
def test_change_directory(dest_dir_name, cur_dir_path, expected_dir_path):
    # GIVEN
    root_dir = Node("", NodeType.directory)
    subdir = Node("subdir", NodeType.directory, parent=root_dir)
    subsubdir = Node("subsubdir", NodeType.directory, parent=subdir)

    dir_map = {root_dir.path: root_dir, subdir.path: subdir, subsubdir.path: subsubdir}

    # WHEN
    new_dir = change_directory(dest_dir_name, dir_map[cur_dir_path], dir_map)

    # THEN
    assert new_dir == dir_map[expected_dir_path]
