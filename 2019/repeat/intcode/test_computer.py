from collections import deque

import pytest

from intcode4 import Computer


def test_init_copies_data():
    # GIVEN: a Computer with data
    data = [1, 2, 3]
    computer = Computer(data)
    original_value = data[0]

    # WHEN: original data is changed
    data[0] += 1

    # THEN: computer memory is unchanged
    memory = computer.dump()
    assert memory[0] == original_value
    assert memory != data
    assert computer._code == data


def test_init_default_buffers():
    # GIVEN: a Computer with no custom buffers
    data = [1, 2, 3]
    computer = Computer(data)

    # THEN: empty deque instances assigned to buffers
    input_buffer = computer.get_input_buffer()
    output_buffer = computer.get_output_buffer()
    assert isinstance(input_buffer, deque)
    assert isinstance(output_buffer, deque)
    assert len(input_buffer) == len(output_buffer) == 0


def test_init_custom_buffers():
    # GIVEN: a Computer with custom buffers
    data = [1, 2, 3]
    input_buffer = deque([456])
    output_buffer = deque([789])
    computer = Computer(
        data,
        custom_input_buffer=input_buffer,
        custom_output_buffer=output_buffer,
    )

    # THEN: populated deque instances assigned to buffers
    assert computer.get_input_buffer() == input_buffer
    assert computer.get_output_buffer() == output_buffer


def test_initialize():
    # GIVEN
    data = [1, 2, 3]
    computer = Computer(data)
    new_init_data = {0: 7, 2: 8}

    # Adjust values to be reset
    computer._instruction_pointer = 1
    computer._relative_base = 1

    # WHEN
    computer.initialize(new_init_data)

    # THEN
    assert computer._code == data
    assert computer._instruction_pointer == 0
    assert computer._relative_base == 0
    memory = computer.dump()
    for idx, val in new_init_data.items():
        assert memory[idx] == val


@pytest.mark.parametrize(
    "original, final",
    [
        pytest.param(
            [1, 5, 6, 4, 0, 44, 55],
            [1, 5, 6, 4, 99, 44, 55],
            id="add-position-mode",
        ),
        pytest.param(
            [109, 1, 2201, 6, 7, 6, 0, 44, 55],
            [109, 1, 2201, 6, 7, 6, 99, 44, 55],
            id="add-relative-mode",
        ),
        pytest.param(
            [1101, 44, 55, 4, 0],
            [1101, 44, 55, 4, 99],
            id="add-immediate-mode",
        ),
        pytest.param(
            [2, 5, 6, 4, 0, 9, 11],
            [2, 5, 6, 4, 99, 9, 11],
            id="multiply-position-mode",
        ),
        pytest.param(
            [109, 1, 2202, 6, 7, 6, 0, 9, 11],
            [109, 1, 2202, 6, 7, 6, 99, 9, 11],
            id="multiply-relative-mode",
        ),
        pytest.param(
            [1102, 9, 11, 4, 0],
            [1102, 9, 11, 4, 99],
            id="multiply-immediate-mode",
        ),
    ]
)
def test_arithmetic(original, final):
    # GIVEN
    computer = Computer(original)

    # WHEN
    result = computer.run()

    # THEN
    assert computer.dump() == final
    assert result == 0


def test_input():
    # GIVEN
    data = [3, 4, 3, 5, 0]  # Overwrite 0 with 99, write 88 beyond initial program
    input_buffer = deque([99, 88, 77])
    computer = Computer(
        data,
        io_src=Computer.MEMBUF_IO_SRC,
        custom_input_buffer=input_buffer,
    )

    # WHEN
    result = computer.run()

    assert computer.dump() == [3, 4, 3, 5, 99, 88]
    assert list(computer.get_input_buffer()) == [77]
    assert result == 0


@pytest.mark.parametrize(
    "data, output", [
        pytest.param([4, 5, 4, 4, 99], [0, 99], id="position-mode"),
        pytest.param([104, 2, 99], [2], id="immediate-mode"),
    ]
)
def test_output(data, output):
    # GIVEN
    computer = Computer(
        data,
        io_dest=Computer.MEMBUF_IO_DEST,
        custom_output_buffer=deque(),
    )

    # WHEN
    result = computer.run()

    # THEN
    assert list(computer.get_output_buffer()) == output
    assert result == 0


@pytest.mark.parametrize(
    "data, instruction_pointer",
    [
        pytest.param([5, 1, 3, 4, 99], 4, id="jump-if-true-position-true"),
        pytest.param([5, 2, 0, 99], 3, id="jump-if-true-position-false"),
        pytest.param([1105, 1, 4, 0, 99], 4, id="jump-if-true-immediate-true"),
        pytest.param([1105, 0, 0, 99], 3, id="jump-if-true-immediate-false"),
        pytest.param([6, 1, 0, 99], 3, id="jump-if-false-position-true"),
        pytest.param([6, 3, 0, 0, 0, 0, 99], 6, id="jump-if-false-position-false"),
        pytest.param([1106, 1, 0, 99], 3, id="jump-if-false-immediate-true"),
        pytest.param([1106, 0, 4, 0, 99], 4, id="jump-if-false-immediate-false"),
    ]
)
def test_jump_if_bool(data, instruction_pointer):
    # GIVEN
    computer = Computer(data)

    # WHEN
    result = computer.run()

    # THEN
    assert computer._instruction_pointer == instruction_pointer
    assert result == 0


@pytest.mark.parametrize(
    "original, final",
    [
        pytest.param([7, 1, 2, 5, 99, 0], [7, 1, 2, 5, 99, 1], id="less-than-position-mode-true"),
        pytest.param([7, 4, 2, 5, 99, 1], [7, 4, 2, 5, 99, 0], id="less-than-position-mode-false"),
        pytest.param([1107, 8, 9, 5, 99, 0], [1107, 8, 9, 5, 99, 1], id="less-than-immediate-mode-true"),
        pytest.param([1107, 9, 8, 5, 99, 1], [1107, 9, 8, 5, 99, 0], id="less-than-immediate-mode-false"),
        pytest.param([8, 0, 0, 5, 99, 0], [8, 0, 0, 5, 99, 1], id="equal-to-position-mode-true"),
        pytest.param([8, 1, 2, 5, 99, 1], [8, 1, 2, 5, 99, 0], id="equal-to-position-mode-false"),
        pytest.param([1108, 8, 8, 5, 99, 0], [1108, 8, 8, 5, 99, 1], id="equal-to-immediate-mode-true"),
        pytest.param([1108, 8, 9, 5, 99, 1], [1108, 8, 9, 5, 99, 0], id="equal-to-immediate-mode-false"),
    ]
)
def test_compare(original, final):
    # GIVEN
    computer = Computer(original)

    # WHEN
    result = computer.run()

    # THEN
    assert computer.dump() == final
    assert result == 0


@pytest.mark.parametrize(
    "data, offset",
    [
        pytest.param([109, 1, 99], 1, id="position-mode"),
        pytest.param([109, 1, 209, 0, 99], 2, id="relative-mode"),
        pytest.param([9, 3, 99, 1], 1, id="immediate-mode"),
    ]
)
def test_rel_base_adjust(data, offset):
    # GIVEN
    computer = Computer(data)

    # WHEN
    result = computer.run()

    # THEN
    assert computer._relative_base == offset
    assert result == 0
