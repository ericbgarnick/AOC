from unittest import TestCase, main

from day16.dance import Dance


class TestDay16(TestCase):
    def setUp(self):
        start_code = 97
        alph_len = 16
        self.data = [chr(code_pt) for code_pt in
                     range(start_code, start_code + alph_len)]
        self.dance = Dance(self.data)

    def test_spin(self):
        results_for_spins = {'s0': 'abcdefghijklmnop',
                             's1': 'pabcdefghijklmno',
                             's16': 'abcdefghijklmnop',
                             's15': 'bcdefghijklmnopa',
                             's17': 'pabcdefghijklmno'}
        for instr, result in results_for_spins.items():
            self.dance.reset()
            self.dance.call_dance(instr)
            self.assertEqual(self.dance.dancers, list(result))

    def test_exchange(self):
        results_from_exchanges = {'abcdefghijklmnop': 'x0/0',
                                  'pbcdefghijklmnoa': 'x0/15',
                                  'bacdefghijklmnop': 'x0/1',
                                  'abcdefghijklmnpo': 'x14/15'}
        for result, instr in results_from_exchanges.items():
            self.dance.reset()
            self.dance.call_dance(instr)
            self.assertEqual(self.dance.dancers, list(result))

    def test_partner(self):
        results_from_partners = {'abcdefghijklmnop': 'pa/a',
                                 'pbcdefghijklmnoa': 'pa/p',
                                 'bacdefghijklmnop': 'pa/b',
                                 'abcdefghijklmnpo': 'po/p'}
        for result, instr in results_from_partners.items():
            self.dance.reset()
            self.dance.call_dance(instr)
            self.assertEqual(self.dance.dancers, list(result))

    def test_fast_dance(self):
        original = 'abcdefghijklmnop'
        final = 'ofglpmanecbdhkij'
        conversion = [final.index(el) for el in original]
        self.dance.fast_dance(conversion)
        self.assertEqual(self.dance.dancers, list(final))


if __name__ == '__main__':
    main()
