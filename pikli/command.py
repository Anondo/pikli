import sys

class Command(object):

    def __init__(self , use , short = None , long = None , run = None):
        self.use = use
        self.short = short
        self.long = long
        self.run = run
        self.commands = []
        self.parent = None
        self.arguments = 0

    def execute(self):
        self.arguments = self.__parent_count()

        self.__check_run()

        self.__check_short()

        self.__check_commands()

        self.__check_sub_commands()


    def add_command(self , cmnd):
        cmnd.parent = self
        self.commands.append(cmnd)

    def __parent_count(self):
        count = 0
        parent = self
        while parent:
            count += 1
            parent = parent.parent
        return count

    def __check_run(self):
        if self.run:
            try:
                self.run(self , sys.argv)
            except Exception:
                pass
    def __check_short(self):
        if self.short and not self.run and len(sys.argv) == self.arguments:
            print(self.short + "\n\n\n")
    def __check_commands(self):
        if self.commands and len(sys.argv) == self.arguments:
            print("Available Commands:")
            for command in self.commands:
                print("{}            {}".format(command.use,command.short))
    def __check_sub_commands(self):
        if len(sys.argv) > self.arguments and self.commands:
            for command in self.commands:
                if command.use == sys.argv[self.arguments]:
                    command.execute()
                    break
