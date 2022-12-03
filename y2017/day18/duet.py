from typing import Union, Iterable, Tuple, List, Callable, Optional
from collections import deque


class NaiveDuet:
    def __init__(self, raw_instructions: Iterable[str]):
        self._last_played = 0
        self._registers = {}

        self._instructions = self._parse_instructions(raw_instructions)
        self._instruction_index = -1

    def run(self):
        while -2 < self._instruction_index < len(self._instructions):
            self._instruction_index += 1
            fn, args = self._instructions[self._instruction_index]
            try:
                fn(*args)
            except KeyError:
                # Sometimes an operation may be called on a register
                # that hasn't been set yet
                pass

    def _parse_instructions(self, raw_instructions: Iterable[str]) -> \
            List[Tuple[Callable, List]]:
        parsed = []
        for instr_string in raw_instructions:
            fn, *rest = instr_string.split()
            args = [rest[0]]
            if len(rest) > 1:
                raw_val = rest[1]
                val = int(raw_val) if raw_val.strip('-').isnumeric() else raw_val
                args.append(val)
            parsed.append((self.__getattribute__('_' + fn), args))
        return parsed

    def _snd(self, register: str):
        self._last_played = self._registers[register]

    def _set(self, register: str, value: Union[int, str]):
        try:
            value = self._registers[value]
        except KeyError:
            pass

        self._registers[register] = value

    def _add(self, register: str, increment: Union[int, str]):
        try:
            increment = self._registers[increment]
        except KeyError:
            pass

        self._registers[register] += increment

    def _mul(self, register: str, factor: Union[int, str]):
        try:
            factor = self._registers[factor]
        except KeyError:
            pass

        self._registers[register] *= factor

    def _mod(self, register: str, dividend: Union[int, str]):
        try:
            dividend = self._registers[dividend]
        except KeyError:
            pass

        self._registers[register] %= dividend

    def _rcv(self, register: str):
        if self._registers[register]:
            self._instruction_index = -2
            print("PLAYED:", self._last_played)

    def _jgz(self, register: str, offset: Union[int, str]):
        try:
            offset = self._registers[offset]
        except KeyError:
            pass

        if self._registers[register] > 0:
            # print("VALUE IS:", self._registers[register])
            # Less one because of auto-increment
            self._instruction_index += (offset - 1)


class RealDuet(NaiveDuet):

    def __init__(self, raw_instructions: Iterable[str], program_id: int,
                 partner=None):
        super().__init__(raw_instructions)
        self._pid = program_id
        self._registers['p'] = program_id
        self._partner = partner             # type: Optional[RealDuet]
        self._buffer = deque()
        self._stopped = False
        # Indicates if this program was able to advance to a new instruction
        self._advanced = True
        self._snd_count = 0

    @property
    def send_count(self):
        return self._snd_count

    @property
    def done(self):
        return not self._advanced

    def set_partner(self, partner):
        self._partner = partner

    def run(self):
        if self._partner is None:
            raise Exception("Missing partner for RealDuet")

        # in_order = sorted(self._buffer)
        # if in_order and in_order == list(self._buffer):
        #     print("\nDONE at {}\n".format(self._partner.send_count))

        run_count = 0
        self._stopped = False

        while not self._stopped:
            self._instruction_index += 1
            fn, args = self._instructions[self._instruction_index]
            # print("{} at {} doing {} with {}".format(self._pid, self._instruction_index, fn, args))
            try:
                fn(*args)
                run_count += 1
            except KeyError:
                # Sometimes an operation may be called on a register
                # that hasn't been set yet
                pass

        # print("\n++++++++++++++++\n{} PROCESSED: {}\n++++++++++++++++\n"
        #       .format(self._pid, run_count))
        # Was able to run more than the same instruction as last time
        self._advanced = run_count > 1

    def enqueue(self, value: int):
        self._buffer.append(value)

    def _rcv(self, register: str):
        try:
            value = self._buffer.popleft()
            self._registers[register] = value
        except IndexError:
            # Move back to re-read this instruction
            self._instruction_index -= 1
            self._stopped = True

    def _snd(self, value: str):
        try:
            value = self._registers[value]
        except KeyError:
            pass

        # print("{} SENDING {} at {}".format(self._pid, value, self._instruction_index))

        self._partner.enqueue(value)
        self._snd_count += 1
