#!/usr/bin/env python3

from . import Utils
from secrets import choice, randbelow
from re import split


class Password:
    """
    Password generator
    
    :param lst: Word list filename
    :type lst: str
    :param mnw: Minimum word length
    :type mnw: int
    :param mxw: Maximum word length
    :type mxw: int
    :param wrd: Number of words in the generated password
    :type wrd: int
    :param sep: Separator between words
    :type sep: str
    :param cap: Capitalize words option
    :type cap: bool
    :param sym: Add symbol option
    :type sym: bool
    :param config: Configuration
    :type config: dict
    """
    def __init__(
        self, lst, mnw, mxw, wrd, sep, cap, num, sym,
        config
    ):
        """
        Constructor
        """
        # Word list
        self.lst = split(r"\s+", open(lst, "r").read())
        # Minimum word length
        self.mnw = mnw
        # Maximum word length
        self.mxw = mxw
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
        
        :return: List of words to use in password
        :rtype: list
        """
        # Filter word list based on length
        lexicon = []
        for word in self.lst:
            if len(word) >= self.mnw and len(word) <= self.mxw:
                lexicon.append(word)
        return lexicon

    def _form_sym_list(self):
        """
        Form the list of possible symbols to add
        
        :return: List of symbols to use in password
        :rtype: list
        """
        return [symbol for symbol in Utils.SYMBOLS if self.config[symbol]]

    def _add_num_sym(self, sym_list, num_ind, sym_ind, ind):
        """
        Add a number and symbol
        
        :param sym_list: List of symbols
        :type sym_list: list
        :param num_ind: Index of number insertion into password
        :type num_ind: int
        :param sym_ind: Index of symbol insertion into password
        :type sym_ind: int
        :param ind: Index of word in password
        :type ind: int
        :return: String to add to password
        :rtype: str
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
        Generate password of `wrd` words from lexicon
        
        :return: Generated password
        :rtype: str
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
