import sys

class Command(object):

    def __init__(self , use , short = None , long = None , run = None , arguments = 0):
        self.use = use
        self.short = short
        self.long = long
        self.run = run
        self.arguments = arguments
        self.commands = []
        self.parent = None

    def execute(self):
        if self.run:
            if self.arguments:
                if not self.parent:
                    self.run(sys.argv[self.arguments])
                else:
                    self.run(sys.argv[self.parent.arguments+self.arguments+1])
            else:
                self.run()
        if self.short and not self.run and len(sys.argv) == 1:
            print(self.short)

        if self.commands and len(sys.argv) == 1:
            print("Available Commands            Usage")
            for command in self.commands:
                print("{}                     {}".format(command.use,command.short))
        if len(sys.argv) > 1 and self.commands:
            for command in self.commands:
                if not self.parent:
                    if command.use == sys.argv[1]:
                        command.execute()
                        break
                else:
                    if command.use == sys.argv[self.parent.arguments+1]:
                        command.execute()
                        break

    def add_command(self , cmnd):
        cmnd.parent = self
        self.commands.append(cmnd)
