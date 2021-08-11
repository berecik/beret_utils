import math
from dataclasses import dataclass
from random import choice
from typing import Optional
from typing import Sequence


@dataclass
class Codes:

    DEFAULT_CHARS = '23456789abcdefghijkmnrstuvwxyz'
    chars: Sequence = DEFAULT_CHARS
    count: Optional[int] = None

    @property
    def chars_len(self):
        return len(self.chars)

    def __call__(
            self,
            length: Optional[int] = None,
            count: Optional[int] = None
    ):
        if length is None:
            if count is None:
                count = self.count
            length = self.code_len(count)
        return "".join([choice(self.chars) for _ in range(length)])

    def code_len(self, count):
        length = math.log(count, self.chars_len)
        return int(length) + 1


def get_code(*args, **kwargs):
    if "chars" in kwargs:
        chars = kwargs.pop("chars")
    else:
        chars = Codes.DEFAULT_CHARS
    codes_generator = Codes(chars=chars)
    return codes_generator(*args, **kwargs)
