import os
from unittest import TestCase
from beret_utils.random_code import Codes, get_code


class TestCode(TestCase):
    def setUp(self):
        self.codes = set()
        self.count = len(Codes.DEFAULT_CHARS)
        # if count of codes is one less than length of chars
        # length of codes should be exactly one
        self.get_code = Codes(count=self.count-1)

    def test_codes(self):
        for i in range(self.count):
            # let gamble each of chars
            while True:
                code = self.get_code()
                if code not in self.codes:
                    self.codes.add(code)
                    break

        for c in Codes.DEFAULT_CHARS:
            # for codes length one, each char of chars
            # should be in codes set
            self.assertIn(c, self.codes)
