from typing import List, Set


class Dance:
    def __init__(self, participants: List[str]):
        self.original_list = participants
        self.original = ''.join(participants)
        self.dancers = participants

    def reset(self):
        self.dancers = list(self.original)

    def call_dance(self, instructions: str,
                   allowed_instructions: Set[str]=None):
        """Call private dance methods for each comma-separated instruction in
        self.instructions."""
        call_map = {'s': self._spin, 'x': self._exchange, 'p': self._partner}
        for instruction in instructions.split(','):
            instr_type = instruction[0]
            instr_val = instruction[1:]
            if allowed_instructions and instr_type not in allowed_instructions:
                continue
            call_fn = call_map[instr_type]
            call_fn(instr_val)

    def fast_dance(self, conversion: List[int]):
        """Move elements of self.dancers to the indices given in conversion"""
        result = ['x' for _ in range(len(self.dancers))]
        for idx, destination in enumerate(conversion):
            result[destination] = self.dancers[idx]
        self.dancers = result

    def _spin(self, spin: str):
        """Rotate n elements in self.dancers from the end to the front"""
        n = int(spin)
        if n > 0:
            real_n = n % len(self.dancers)
            self.dancers = self.dancers[-real_n:] + self.dancers[:-real_n]

    def _exchange(self, exchange: str):
        """Swap elements of self.dancers at pos_a and pos_b"""
        pos_a, pos_b = [int(pos) for pos in exchange.split('/')]
        self.dancers[pos_a], self.dancers[pos_b] = (self.dancers[pos_b],
                                                    self.dancers[pos_a])

    def _partner(self, partner: str):
        """Swap elements el_a and el_b of self.dancers"""
        el_a, el_b = [el for el in partner.split('/')]
        pos_a = self.dancers.index(el_a)
        pos_b = self.dancers.index(el_b)
        self._exchange('{}/{}'.format(pos_a, pos_b))
