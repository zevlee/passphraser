#!/usr/bin/env python3

from lib.utils import Utils
from secrets import choice, randbelow
from re import split


class Password:

    def __init__(
        self, lst, min, max, wrd, sep, cap, num, sym,
        config
    ):
        # Word list
        self.lst = split(r"\s+", open(lst, "r").read())
        # Minimum word length
        self.min = min
        # Maximum word length
        self.max = max
        # Number of words
        self.wrd = wrd
        # Separator
        self.sep = sep
        # Capitalize
        self.cap = cap
        # Add number
        self.num = num
        # Add symbol
        self.sym = sym
        # Config directory
        self.config = config

    def _form_lexicon(self):
        """
        Form lexicon from which words are chosen to create passwords
        """
        # Filter word list based on length
        lexicon = []
        for word in self.lst:
            if len(word) >= self.min and len(word) <= self.max:
                lexicon.append(word)
        return lexicon

    def _form_sym_list(self):
        """
        Form the list of possible symbols to add
        """
        return [symbol for symbol in Utils.SYMBOLS if self.config[symbol]]

    def _add_num_sym(self, sym_list, num_ind, sym_ind, ind):
        """
        Add a number and symbol
        """
        result = ""
        # half the time, adding a number is prioritized
        if choice([True, False]):
            if self.num and ind == num_ind:
                num = str(randbelow(10))
                result += f"{num}{self.sep}"
            if self.sym and ind == sym_ind:
                try:
                    sym = choice(sym_list)
                except IndexError:
                    sym = ""
                result += f"{sym}{self.sep}"
        else:
            if self.sym and ind == sym_ind:
                try:
                    sym = choice(sym_list)
                except IndexError:
                    sym = ""
                result += f"{sym}{self.sep}"
            if self.num and ind == num_ind:
                num = str(randbelow(10))
                result += f"{num}{self.sep}"
        return result

    def generate_password(self):
        """
        Generates password of `wrd` words from lexicon
        """
        lexicon = self._form_lexicon()
        sym_list = self._form_sym_list()

        result = ""
        # Choose random points to add a number and symbol
        num_ind = randbelow(self.wrd + 1)
        sym_ind = randbelow(self.wrd + 1)

        for i in range(self.wrd):
            # Num and sym
            result += self._add_num_sym(sym_list, num_ind, sym_ind, i)
            # Word
            word = choice(lexicon)
            if self.cap:
                result += f"{word.capitalize()}{self.sep}"
            else:
                result += f"{word.lower()}{self.sep}"
        # Num and sym end case
        result += self._add_num_sym(sym_list, num_ind, sym_ind, self.wrd)
        if self.sep != "":
            result = result[:-len(self.sep)]
        return result
