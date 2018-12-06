import sys
from .helper import add_int_flag



class IntFlag(object):

    def __init__(self , flag_name , flag_use , default , description):
        self.flag_name = flag_name
        self.flag_use = flag_use
        self.default = int(default)
        self.description = description

class Flag(object):

    def __init__(self):
        self.int_flags = []

    def intp(self , flagname , flaguse , default , description):
        int_flag = IntFlag(flagname ,"-" + flaguse , default , description)
        self.int_flags.append(int_flag)
        add_int_flag(int_flag)

    def is_flag(self , flag):
        for f in self.int_flags:
            if flag == f.flag_use:
                return True

        return False

    def assign_flag_value(self , flag , value):
        for f in self.int_flags:
            if flag == f.flag_use:
                f.default = int(value)
                break
