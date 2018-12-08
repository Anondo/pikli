"""
  pikli.core
  ~~~~~~~~~~~~~

  Copyright @2018 Ahmad Anondo.  All rights reserved.
  Use of this source code is governed by a MIT-style
  license that can be found in the LICENSE file.

  This module implements the core functions to be used directly from the package

"""

#--------------Functions For Flag--------------#

#global list of flags

int_flags = []
str_flags = []
bool_flags = []

def get_int(flag_name):

    """ returns the integer value for a particular flag

        Args:
            flag_name (str): name of the flag

    """

    for flag in int_flags:
        if flag_name == flag.flag_name:
            return flag.default

    return None


def get_bool(flag_name):

    """ returns the boolean value for a particular flag

        Args:
            flag_name (str): name of the flag

    """

    for flag in bool_flags:
        if flag_name == flag.flag_name:
            return flag.default


    return None


def get_str(flag_name):

    """ returns the string value for a particular flag

        Args:
            flag_name (str): name of the flag

    """

    for flag in str_flags:
        if flag_name == flag.flag_name:
            return flag.default


    return None



def add_flag(flag):

    """ Adds a flag to the gobal list of flags

        Args:
            flag (BaseP): the flag to be added to the list

    """


    if flag.get_type() == "int":
        if get_int(flag.flag_name): #this is to prevent duplicate data
            return
        int_flags.append(flag)
    elif flag.get_type() == "str":
        if get_str(flag.flag_name):
            return
        str_flags.append(flag)
    elif flag.get_type() == "bool":
        if get_bool(flag.flag_name):
            return
        bool_flags.append(flag)


#------------------------X---------------------------#
