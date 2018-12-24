
"""
  pikli.flag
  ~~~~~~~~~~~~~

  Copyright @2018 Ahmad Anondo.  All rights reserved.
  Use of this source code is governed by a MIT-style
  license that can be found in the LICENSE file.

  This module implements all the classes required to create flags
  for a command.


"""





import sys
from .core import add_flag , set_flag_val







class HelpFlag(object):

    def __init__(self , cmd):
        self.flag_name = "help"
        self.flag_use = "-h"
        self.flag_description = "Shows info regarding the command"
        self.cmd = cmd

    def execute(self):

        self.__check_short()
        self.__check_long()
        self.__show_usage()
        self.__check_available_commands()
        self.__check_available_flags()


    def __show_usage(self):

        """ Shows the command's usage on the terminal """

        print("\n\nUsage:")
        print("\t{} [args] [flags] [sub commands]".format(self.cmd.use))


    def __check_short(self):

        """ Checks for a short description & prints it"""

        if self.cmd.short: #if short description provided
            print(self.cmd.short)

    def __check_long(self):

        """ Checks for a long description & prints it"""

        if self.cmd.long: #if long description provided
            print("\n" + self.cmd.long)


    def __check_available_commands(self):

        """ Checks for avaiable commands to display them"""


        if self.cmd.commands: #if commands are available
            print("\n\nAvailable Commands:")
            for command in self.cmd.commands:
                print("{}            {}".format(command.use,command.short))

    def __check_available_flags(self):

        """ Checks for avaiable flags to display them"""

        self.cmd.flag.show_flag_details(self)



class BaseP(object):


    """
        Is herited by the child classes which are the PFlags for the commands

        Attributes:
            flag_name (str): name of the flag

            flag_use (str): the usable name of the flag on the cli

            default (type): the value which the flag holds. Type
                               depends on the type of the flag

            description (str): a description of what the flag does

            type (str): the type of the flag


    """


    def __init__(self , flag_name , flag_use , default , description , type = None):
        self.flag_name = flag_name
        self.flag_use = flag_use
        self.default = default
        self.description = description
        self.type = type

    def get_type(self):

        """ returns the type of the flag in str """

        return self.type



class IntPFlag(BaseP):

    """

        Inherits the BaseP class.

        Converts the default value to int type

    """

    def __init__(self , flag_name , flag_use , default , description = ""):
        super(IntPFlag , self).__init__(flag_name , flag_use , int(default) , description , "int")

class StringPFlag(BaseP):

    """

        Inherits the BaseP class.

        The values are read in string by default by sys.argv

    """

    def __init__(self , flag_name , flag_use , default , description = ""):
        super(StringPFlag , self).__init__(flag_name , flag_use , default , description , "str")

class BoolPFlag(BaseP):

    """

        Inherits the BaseP class.

        Converts the default value to bool type

    """

    def __init__(self , flag_name , flag_use , default = False , description = ""):
        super(BoolPFlag , self).__init__(flag_name , flag_use , bool(default) , description , "bool")

class Flag(object):

    """
        Creates a flag object that provides the creation of flags for a
        particular command

        Attributes:

            int_flags ([]IntPFlag): list of IntPFlags for the command

            str_flags ([]StringPFlag): list of StringPFlags for the command

            bool_flags ([]BoolPFlag): list of BoolPFlags for the command


    """

    def __init__(self):
        self.int_flags = []
        self.str_flags = []
        self.bool_flags = []



    def intp(self , flagname , flaguse , default , description):

        """ creates a integer flag for the command

            See help(pikli.flag.BaseP) for the arguments
         """

        int_flag = IntPFlag(flagname ,"-" + flaguse , default , description) #the flags will be provided with a dash
        self.int_flags.append(int_flag)
        add_flag(int_flag) #adding to the gobal list of flags for the retrieval of values

    def stringp(self , flagname , flaguse , default , description):

        """ creates a string flag for the command

            See help(pikli.flag.BaseP) for the arguments
         """

        str_flag = StringPFlag(flagname , "-" + flaguse , default, description)
        self.str_flags.append(str_flag)
        add_flag(str_flag)

    def boolp(self , flagname , flaguse , description , default = False):

        """ creates a bool flag for the command

            See help(pikli.flag.BaseP) for the arguments
         """

        bool_flag = BoolPFlag(flagname ,"-" + flaguse , default , description)
        self.bool_flags.append(bool_flag)
        add_flag(bool_flag)



    def get_flag(self , flag_use):

        """ returns the requested flag

            Args:
                flag_use (str): the usable name of the flag

        """


        for f in self.int_flags:
            if flag_use == f.flag_use:
                return f

        for f in self.str_flags:
            if flag_use == f.flag_use:
                return f

        for f in self.bool_flags:
            if flag_use == f.flag_use:
                return f

        return None

    def get_flag_by_name(self , flag_name):

        """ returns the requested flag

            Args:
                flag_name (str): the name of the flag

        """


        for f in self.int_flags:
            if flag_name == f.flag_name:
                return f

        for f in self.str_flags:
            if flag_name == f.flag_name:
                return f

        for f in self.bool_flags:
            if flag_name == f.flag_name:
                return f

        return None

    def assign_flag_value(self , flag , value):

        """ assigns value to the provided flag

            Args:
                flag (BaseP): the flag assigned to the command

                value (type): the value to be assigned to the flag.
                              Types depends on the type of the flag

         """

        if flag.get_type() == "int":
            flag.default = int(value)
        else:
            flag.default = value # TODO: a value parameter is provided for BoolPFlag, but the asisgned value is always True. Need to think about it

        set_flag_val(flag , value)

    def show_flag_details(self , help):


        """ Prints all the flag details if available """

        print("\n\nFlags:")
        print("{}, --{}                {}".format(help.flag_use , help.flag_name , help.flag_description))

        if self.int_flags or self.str_flags or self.bool_flags:
            for flag in self.int_flags:
                print("{}, --{} {}               {}".format(flag.flag_use , flag.flag_name , flag.type  , flag.description))
            for flag in self.str_flags:
                print("{}, --{} {}               {}".format(flag.flag_use , flag.flag_name , flag.type  , flag.description))
            for flag in self.bool_flags:
                print("{}, --{} {}               {}".format(flag.flag_use , flag.flag_name , flag.type  , flag.description))





class PersistentFlag(object):

    """
        Creates a flag object that provides the creation of flags for a
        command & all the child commands under it.

        Attributes:

            cmd (pikli.Command): the command using the persistent flag


    """

    def __init__(self , cmd):
        self.cmd = cmd

    def intp(self , flagname , flaguse , default , description):

        """ creates a integer flag for the command & all the sub-commands

            under it

            See help(pikli.flag.BaseP) for the arguments
         """

        int_flag = IntPFlag(flagname ,"-" + flaguse , default , description)

        self.cmd.flags().int_flags.append(int_flag)

        for c in self.cmd.commands:
            c.persistent_flags().intp(flagname , flaguse , default , description)


        add_flag(int_flag) #dont worry about this, duplications will not be added

    def stringp(self , flagname , flaguse , default , description):

        """ creates a string flag for the command & all the sub-commands

            under it

            See help(pikli.flag.BaseP) for the arguments
         """

        str_flag = StringPFlag(flagname ,"-" + flaguse , default , description)

        self.cmd.flags().str_flags.append(str_flag)

        for c in self.cmd.commands:
            c.persistent_flags().stringp(flagname , flaguse , default , description)


        add_flag(str_flag)

    def boolp(self , flagname , flaguse , description , default = False):

        """ creates a bool flag for the command & all the sub-commands

            under it

            See help(pikli.flag.BaseP) for the arguments
         """

        bool_flag = BoolPFlag(flagname ,"-" + flaguse , default , description)

        self.cmd.flags().bool_flags.append(bool_flag)

        for c in self.cmd.commands:
            c.persistent_flags().boolp(flagname , flaguse , description , default)


        add_flag(bool_flag)
