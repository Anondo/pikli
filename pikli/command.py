
"""
  pikli.command
  ~~~~~~~~~~~~~

  Copyright @2018 Ahmad Anondo.  All rights reserved.
  Use of this source code is governed by a MIT-style
  license that can be found in the LICENSE file.

  This module implements the Command class

"""

import sys
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
                           postion in terms of sys.argv
            flag (Flag): the flag object that holds all the flags assigned
                         to the command


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

    def execute(self):

        """ Performs the execution of the command

            Example:
                root_command = pikli.Command(
                        use = "hello",
                        short = "Hello is the  first ever cli app built using pikli",
                )
                root_command.execute()

        """

        self.arg_pos = self.__parent_count()

        self.__check_flags()

        self.__check_run()

        self.__check_short()

        self.__check_available_commands()

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
                self.run(self , sys.argv)
            except Exception:
                pass  # TODO: Add explicit exceptions
    def __check_short(self):

        """ Checks for a short description & prints it"""

        if self.short and not self.run and len(sys.argv) == self.arg_pos: #if short description provided & nothing to run & no args
            print(self.short)
    def __check_available_commands(self):

        """ Checks for avaiable commands to display them"""

        if self.commands and len(sys.argv) == self.arg_pos:
            print("\nAvailable Commands:")
            for command in self.commands:
                print("{}            {}".format(command.use,command.short))
    def __check_sub_commands(self):

        """ Checks for any sub commands from the cli for execution """

        if len(sys.argv) > self.arg_pos and self.commands: #if sub-command sys.argv position is ok & sub-commands actually exists
            for command in self.commands:
                if command.use == sys.argv[self.arg_pos]: #if the sub-command.use is the command provided
                    command.execute()
                    break
    def __check_flags(self):

        """ Checks for any flags to assign value to them """

        for i , arg in enumerate(sys.argv[self.arg_pos:]): #using enumerate to get the index of the argument
            flag = self.flag.get_flag(arg) #getting the actual flag
            if flag:
                if flag.get_type() == "bool":
                    self.flag.assign_flag_value(flag , True)#if the flag is bool,the value must be true
                else:
                    self.flag.assign_flag_value(flag , sys.argv[(self.arg_pos+i)+1])#sending the flag with the value(they will be side by side)




                    
