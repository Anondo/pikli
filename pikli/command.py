
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

from .flag import Flag , PersistentFlag , HelpFlag



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
            pos (int): absolute position relative to parent
            parents (int): number of parent commands to determine the argument
                           postion in terms of self.argv
            flag (Flag): the flag object that holds all the flags assigned
                         to the command

            persistent_flag (PersistentFlag): the persistent flag object that
                                              helps create all the flags for
                                              the command

            flag_collection (collections.namedtuple): a collection to store the
                                                      flag_use & value of that
                                                      flag
            argv ([]sys.argv): a copy of sys.argv

            help_flag (HelpFlag): the help flag


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
        self.pos = 0
        self.parents = 0
        self.flag = Flag()
        self.persistent_flag = PersistentFlag(self)
        self.flag_collection = collections.namedtuple("flag" , ["flag_use" , "value"])
        self.argv = []

        self.help_flag = HelpFlag(self)

    def execute(self):

        """ Performs the execution of the command

            Example:
                root_command = pikli.Command(
                        use = "hello",
                        short = "Hello is the  first ever cli app built using pikli",
                )
                root_command.execute()

        """

        self.parents = self.__parent_count()

        self.pos = self.parents - 1

        self.argv = sys.argv[self.pos:]

        self.__clean_argv()


        if not self.__help_flag():


            self.__check_flags()

            self.__check_run()

            self.__check_sub_commands()

        if not self.run and len(self.argv) == self.pos:#if nothing to run & no args
            self.help_flag.execute() #then show help


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
    def persistent_flags(self):

        """ returns the flag object that holds all the persistent flags for the command """

        return self.persistent_flag


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
    def __clean_argv(self):

        """

            Strips the argv list of any unwanted values. Specially, parent flags

        """
        while self.argv[0] != self.use and self.argv[0] != sys.argv[0]:#while there are unwanted values at the start of the list && not parent(because if parent, the starting value would be the script name)
            self.argv.pop(0)
    def __is_sub_command(self ,arg):

        """

            Determines if the argument provided is a sub-command or not

            Args:
                arg (str): a command line argument

            Returns:
                True/False (bool)

        """

        for cmnd in self.commands:
            if arg == cmnd.use:
                return True
        return False

    def __help_flag(self):


        """

            determines if help flag for the command is provided or not

            Returns:
                True/False

        """


        help_flag_found = False
        own_help_flag = True

        for arg in self.argv[self.pos: ]:
            if arg == "-h": #looking for any help flags
                help_flag_found = True
                self.argv.pop(self.argv.index(arg))
                break
            if self.__is_sub_command(arg): #looking for any other commands before the help flag
                own_help_flag  = False    #which determines if the help flag belongs to this command or not
                break
            if not own_help_flag:
                break

        if help_flag_found:
            self.help_flag.execute()
            return True
        return False


    def __check_run(self):

        """ Checks for a run method & acts accordingly """

        if self.run:
            try:
                self.run(self.argv[1:]) # sending the list from index 1 because the first value is the command name
            except Exception as Argument:
                print("ValueError: ", Argument)  # TODO: Add explicit exceptions


    def __check_sub_commands(self):

        """ Checks for any sub commands from the cli for execution """

        sub_command_provided = False

        for arg in self.argv:
            if self.__is_sub_command(arg):
                sub_command_provided = True
                break

        if self.commands and sub_command_provided: #if sub-command self.argv position is ok & sub-commands actually exists
            for command in self.commands:
                if command.use in self.argv: #if the sub-command.use is the command provided
                    command.execute()
                    return
            print("CommandError: No such commands")


    def __parse_flags(self , flag_list):


        """

           Parses the flags with along with their values from the argv list.

           Args:
                flag_list ([]flag_collection): a list of flag_collection

        """

        for i , arg in enumerate(self.argv):
            if self.__is_sub_command(arg):#if a sub command is detected
                break   #then it means no more flags for this command
            if arg[0] == "-":
                flag = self.flag.get_flag(arg)
                if flag:
                    if flag.get_type() == "bool":
                        flag_list.append(self.flag_collection(arg , True))
                        self.argv.pop(i)
                        self.__parse_flags(flag_list)#recursion because, need to start looking for flags after pop occurs to get the right index numbers from enumerate
                    else:
                        flag_list.append(self.flag_collection(arg , self.argv[i+1]))#assigning the flag with its value
                        self.argv.pop(i)
                        self.argv.pop(i) #after popping the value index becomes the current index
                        self.__parse_flags(flag_list)


    def __parse_valid_flags(self):

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

        self.__parse_flags(flags)


        return flags


    def __check_flags(self):

        """ Checks for any flags to assign value to them """

        flag_nv_list = self.__parse_valid_flags()


        for f in flag_nv_list:
            flag = self.flag.get_flag(f.flag_use)
            if flag:
                if flag.get_type() == "bool":
                    self.flag.assign_flag_value(flag , True)#if the flag is bool,the value must be true
                else:
                    self.flag.assign_flag_value(flag , f.value)#sending the flag with the value(they will be side by side)
