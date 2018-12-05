import sys
import pikli


def greet(*args):
    print("Hello {} how are you".format(args[0]))

root_command = pikli.Command(
        use = "hello",
        short = "Hello is the  first ever cli app made with pikli",
)

child_command = pikli.Command(
        use = "greet",
        short = "greets the user",
        arguments = 1,
        run = greet
)

root_command.add_command(child_command)


root_command.execute()
