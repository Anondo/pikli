
"""
  pikli.command
  ~~~~~~~~~~~~~

  Copyright @2018 Ahmad Anondo.  All rights reserved.
  Use of this source code is governed by a MIT-style
  license that can be found in the LICENSE file.

  This module implements the Command class

"""

import sys
import collections

from .flag import Flag



class Command(object):

    """
        Creates a command object that provides the execution of the cli commands
        & command chaining

        Attributes:
            use (str): the name of the command (mandatory)
            short (str): short description of the command
            long (str): long description of the command
            run (str): the method to run when the command is executed
            commands ([]Command): list of sub-commands
            parent (Command): the parent command
            arg_pos (int): number of parent commands to determine the argument
                           postion in terms of self.argv
            flag (Flag): the flag object that holds all the flags assigned
                         to the command

            flag_collection (collections.namedtuple): a collection to store the
                                                      flag_use & value of that
                                                      flag
            argv ([]sys.argv): a copy of sys.argv


        Example:

            root_command = pikli.Command(
                    use = "hello",
                    short = "Hello is the  first ever cli app built using pikli",
            )


    """

    def __init__(self , use , short = None , long = None , run = None):
        self.use = use
        self.short = short
        self.long = long
        self.run = run
        self.commands = []
        self.parent = None
        self.arg_pos = 0
        self.flag = Flag()
        self.flag_collection = collections.namedtuple("flag" , ["flag_use" , "value"])
        self.argv = []

    def execute(self):

        """ Performs the execution of the command

            Example:
                root_command = pikli.Command(
                        use = "hello",
                        short = "Hello is the  first ever cli app built using pikli",
                )
                root_command.execute()

        """


        self.argv = sys.argv[:]

        self.arg_pos = self.__parent_count()

        self.__check_flags()

        self.__check_run()

        self.__check_short()

        self.__check_long()

        self.__check_available_commands()

        self.__check_available_flags()

        self.__check_sub_commands()


    def add_command(self , cmnd):

        """ Adds a sub command under the current command

            Args:
                cmnd (Command): the command to be added as the sub-command

            Example:
                root_command = pikli.Command(
                        use = "hello",
                        short = "Hello is the  first ever cli app built using pikli",
                )

                migration_command = pikli.Command(
                        use = "migration",
                        short = "Runs Database migrations"
                )
                root_command.add_command(migration_command)

        """

        cmnd.parent = self
        self.commands.append(cmnd)


    def flags(self):

        """ returns the flag object that holds all the flags for the command """

        return self.flag


    def __parent_count(self):

        """ Calculates the number of parents in the whole chain & returns the
            count
        """

        count = 0
        parent = self #a single node is still a parent without a child
        while parent:
            count += 1
            parent = parent.parent
        return count

    def __check_run(self):

        """ Checks for a run method & acts accordingly """

        if self.run:
            try:
                self.run(self , self.argv)
            except Exception:
                pass  # TODO: Add explicit exceptions
    def __check_short(self):

        """ Checks for a short description & prints it"""

        if self.short and not self.run and len(self.argv) == self.arg_pos: #if short description provided & nothing to run & no args
            print(self.short)

    def __check_long(self):

        """ Checks for a long description & prints it"""

        if self.long and not self.run and len(self.argv) == self.arg_pos: #if long description provided & nothing to run & no args
            print("\n" + self.long)


    def __check_available_commands(self):

        """ Checks for avaiable commands to display them"""


        if self.commands and len(self.argv) == self.arg_pos:
            print("\n\nAvailable Commands:")
            for command in self.commands:
                print("{}            {}".format(command.use,command.short))

    def __check_available_flags(self):

        """ Checks for avaiable flags to display them"""

        if not self.run and len(self.argv) == self.arg_pos:
            self.flag.show_flag_details()

    def __check_sub_commands(self):

        """ Checks for any sub commands from the cli for execution """

        if len(self.argv) > self.arg_pos and self.commands: #if sub-command self.argv position is ok & sub-commands actually exists
            for command in self.commands:
                if command.use == self.argv[self.arg_pos]: #if the sub-command.use is the command provided
                    command.execute()
                    break


    def __get_isolated_flags(self , flag_list):


        """

           Parses the flags with along with their values from the argv list.

           Args:
                flag_list ([]flag_collection): a list of flag_collection

        """


        for i , arg in enumerate(self.argv):
            if arg[0] == "-":
                if len(self.argv) == i+1 or self.argv[i+1][0] == "-": #if the flag doesnt have a value next to it i.e bool flag
                    flag_list.append(self.flag_collection(arg , True))
                    self.argv.pop(i)
                    self.__get_isolated_flags(flag_list)#recursion because, need to start looking for flags after pop occurs to get the right index numbers from enumerate
                else:
                    flag_list.append(self.flag_collection(arg , self.argv[i+1]))
                    self.argv.pop(i)
                    self.argv.pop(i) #after popping the value index becomes the current index
                    self.__get_isolated_flags(flag_list)

    def __get_valid_flags(self , flag_list):

        """

            Parses the flags which only belongs to the current command.

            Args:
                flag_list ([]flag_collection): a list of flag_collection

        """

        for i , flag in enumerate(flag_list):
            if not self.flag.get_flag(flag.flag_use):#if flag doesnt belong to this command, pop it
                flag_list.pop(i)

    def __get_isolated_valid_flags(self):

        """

            Parses just the flags with their values along with the valid ones
            which only belongs to this command. This is done to remove restrictions
            regarding arguments. For example:

            Before this was added, there was a restriction of using argments
            just after the command name:
                [command] [arg1] [args] [flags....]

            After adding this, users can provide the args wherever they want:
                [command] [flag1] [flag1-value] [arg1] [flag2] [flag2-value] [arg2]



            Returns:
                flags: a list of flag_collection

        """

        flags = []

        self.__get_isolated_flags(flags)
        self.__get_valid_flags(flags)


        return flags


    def __check_flags(self):

        """ Checks for any flags to assign value to them """

        flag_nv_list = self.__get_isolated_valid_flags()

        for f in flag_nv_list:
            flag = self.flag.get_flag(f.flag_use)
            if flag:
                if flag.get_type() == "bool":
                    self.flag.assign_flag_value(flag , True)#if the flag is bool,the value must be true
                else:
                    self.flag.assign_flag_value(flag , f.value)#sending the flag with the value(they will be side by side)
