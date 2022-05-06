#!/usr/bin/env python3

from lib.fn import Fn
from secrets import choice, randbelow
from re import split
from os.path import join
from json import loads


class Password:

    def __init__(self, lst, min, max, wrd, sep, cap, num, sym):
        # word list
        self.lst = split(r"\s+", open(lst, "r").read())
        # minimum word length
        self.min = min
        # maximum word length
        self.max = max
        # number of words
        self.wrd = wrd
        # separator
        self.sep = sep
        # capitalize
        self.cap = cap
        # add number
        self.num = num
        # add symbol
        self.sym = sym

    def _form_lexicon(self):
        """
        Forms lexicon from which words are chosen to create passwords
        """
        # filter self.lst based on length
        lexicon = []
        for word in self.lst:
            if len(word) >= self.min and len(word) <= self.max:
                lexicon.append(word)
        return lexicon

    def _form_sym_list(self):
        with open(join(Fn.conf_dir, "passphraser.json"), "r") as cfg:
            config = loads(cfg.read())
            cfg.close()
        symbols = []
        for symbol in Fn.symbols:
            if config[symbol]:
                symbols.append(symbol)
        sym_list = []
        for char in symbols:
            if char not in self.sep:
                sym_list.append(char)
        return sym_list

    def _add_num_sym(self, sym_list, num_ind, sym_ind, ind):
        result = ""
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

    def password(self):
        """
        Creates password of `wrd` words from lexicon
        """
        lexicon = self._form_lexicon()
        sym_list = self._form_sym_list()

        result = ""
        # choose a random point to add a number
        num_ind = randbelow(self.wrd + 1)
        sym_ind = randbelow(self.wrd + 1)

        for i in range(self.wrd):
            # num and sym
            result += self._add_num_sym(sym_list, num_ind, sym_ind, i)
            # word
            word = choice(lexicon)
            if self.cap:
                result += f"{word.capitalize()}{self.sep}"
            else:
                result += f"{word.lower()}{self.sep}"
        # num and sym end case
        result += self._add_num_sym(sym_list, num_ind, sym_ind, self.wrd)
        if self.sep != "":
            result = result[:-len(self.sep)]
        return result, len(result)
