from opcodes import (addr, addi, mulr, muli, banr,
                     bani, borr, bori, setr, seti, gtrr, gtri, gtir, eqrr, eqri, eqir)


class TestOpcodes:
    def test_addr(self):
        registers = [2, 5, 4, 3]
        instructions = (-1, 0, 2, 3)

        expected_result = [2, 5, 4, 6]

        assert addr(registers, instructions) == expected_result

    def test_addi(self):
        registers = [2, 5, 4, 3]
        instructions = (-1, 0, 2, 3)

        expected_result = [2, 5, 4, 4]

        assert addi(registers, instructions) == expected_result

    def test_mulr(self):
        registers = [2, 5, 4, 3]
        instructions = (-1, 0, 2, 3)

        expected_result = [2, 5, 4, 8]

        assert mulr(registers, instructions) == expected_result

    def test_muli(self):
        registers = [2, 5, 4, 3]
        instructions = (-1, 0, 2, 3)

        expected_result = [2, 5, 4, 4]

        assert muli(registers, instructions) == expected_result

    def test_banr(self):
        registers = [2, 5, 4, 3]
        instructions = (-1, 0, 2, 3)

        expected_result = [2, 5, 4, 0]

        assert banr(registers, instructions) == expected_result

    def test_bani(self):
        registers = [2, 5, 4, 3]
        instructions = (-1, 0, 2, 3)

        expected_result = [2, 5, 4, 2]

        assert bani(registers, instructions) == expected_result

    def test_borr(self):
        registers = [2, 5, 4, 3]
        instructions = (-1, 0, 2, 3)

        expected_result = [2, 5, 4, 6]

        assert borr(registers, instructions) == expected_result

    def test_bori(self):
        registers = [2, 5, 4, 3]
        instructions = (-1, 0, 2, 3)

        expected_result = [2, 5, 4, 2]

        assert bori(registers, instructions) == expected_result

    def test_setr(self):
        registers = [2, 5, 4, 3]
        instructions = (-1, 0, 2, 3)

        expected_result = [2, 5, 4, 2]

        assert setr(registers, instructions) == expected_result

    def test_seti(self):
        registers = [2, 5, 4, 3]
        instructions = (-1, 0, 2, 3)

        expected_result = [2, 5, 4, 0]

        assert seti(registers, instructions) == expected_result

    def test_gtrr_true(self):
        registers = [2, 5, 4, 3]
        instructions = (-1, 2, 0, 3)

        expected_result = [2, 5, 4, 1]

        assert gtrr(registers, instructions) == expected_result

    def test_gtrr_false(self):
        registers = [2, 5, 4, 3]
        instructions = (-1, 0, 2, 3)

        expected_result = [2, 5, 4, 0]

        assert gtrr(registers, instructions) == expected_result

    def test_gtri_true(self):
        registers = [2, 5, 4, 3]
        instructions = (-1, 2, 0, 3)

        expected_result = [2, 5, 4, 1]

        assert gtri(registers, instructions) == expected_result

    def test_gtri_false(self):
        registers = [2, 5, 4, 3]
        instructions = (-1, 0, 3, 3)

        expected_result = [2, 5, 4, 0]

        assert gtri(registers, instructions) == expected_result

    def test_gtir_true(self):
        registers = [2, 5, 4, 3]
        instructions = (-1, 3, 0, 3)

        expected_result = [2, 5, 4, 1]

        assert gtir(registers, instructions) == expected_result

    def test_gtir_false(self):
        registers = [2, 5, 4, 3]
        instructions = (-1, 1, 0, 3)

        expected_result = [2, 5, 4, 0]

        assert gtir(registers, instructions) == expected_result

    def test_eqrr_true(self):
        registers = [2, 5, 2, 3]
        instructions = (-1, 2, 0, 3)

        expected_result = [2, 5, 2, 1]

        assert eqrr(registers, instructions) == expected_result

    def test_eqrr_false(self):
        registers = [2, 5, 4, 3]
        instructions = (-1, 0, 2, 3)

        expected_result = [2, 5, 4, 0]

        assert eqrr(registers, instructions) == expected_result

    def test_eqri_true(self):
        registers = [2, 5, 4, 3]
        instructions = (-1, 2, 4, 3)

        expected_result = [2, 5, 4, 1]

        assert eqri(registers, instructions) == expected_result

    def test_eqri_false(self):
        registers = [2, 5, 4, 3]
        instructions = (-1, 0, 3, 3)

        expected_result = [2, 5, 4, 0]

        assert eqri(registers, instructions) == expected_result

    def test_eqir_true(self):
        registers = [2, 5, 4, 3]
        instructions = (-1, 3, 3, 3)

        expected_result = [2, 5, 4, 1]

        assert eqir(registers, instructions) == expected_result

    def test_eqir_false(self):
        registers = [2, 5, 4, 3]
        instructions = (-1, 1, 0, 3)

        expected_result = [2, 5, 4, 0]

        assert eqir(registers, instructions) == expected_result
