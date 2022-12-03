
class Simplifier:
    def __init__(self, instructions: str):
        self.instructions = instructions
        self.pairs = []
        self.non_pairs = []

    def simplify(self):
        self._sift_pairs()
        self._drop_pair_duplicates()
        self.instructions = ','.join(self.pairs + self.non_pairs)

    def _sift_pairs(self):
        """Split instructions in self.instructions into
        pairs and non_pairs depending on instruction type."""
        self.pairs = []
        self.non_pairs = []
        for instr in self.instructions.split(','):
            if instr.startswith('p'):
                self.pairs.append(instr)
            else:
                self.non_pairs.append(instr)

        print("PAIR COUNT:", len(self.pairs))
        print("NON-PAIR COUNT:", len(self.non_pairs))
