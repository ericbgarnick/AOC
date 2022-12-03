class Spinlock:
    def __init__(self, steps: int, cycles: int, remember_first: bool=False):
        self.steps = steps
        self.cycles = cycles
        self.remember_first = remember_first

        self.cur_position = 0
        self.cur_cycle = 0

        self.buffer = [0]
        self.first_val = 0

    def consume(self):
        for _ in range(self.cycles):
            # print("At {} in {}".format(self.cur_position, self.buffer))
            self.cur_cycle += 1
            self._execute_cycle()

    def _execute_cycle(self):
        self._go_to_next_position()
        if self.remember_first:
            self._save_first()
        else:
            self._insert_next_value()
        self._advance_position()

    def _go_to_next_position(self):
        steps_to_take = self.steps % self.cur_cycle
        abs_new_position = self.cur_position + steps_to_take
        self.cur_position = abs_new_position % self.cur_cycle

    def _save_first(self):
        if not self.cur_position:
            self.first_val = self.cur_cycle

    def _insert_next_value(self):
        self.buffer.insert(self.cur_position + 1, self.cur_cycle)

    def _advance_position(self):
        # Buffer size is now cur_cycle + 1
        self.cur_position = (self.cur_position + 1) % (self.cur_cycle + 1)
