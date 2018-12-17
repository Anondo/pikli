import pikli


def start_server(args):
    print("Hello {}".format(args[0] + args[1]))
    if pikli.get_bool("verbose"):
        print("Showing details")
    print("Server starting at: {}".format(pikli.get_int("port")))

def greeter(args):
    print("Hi {}".format(args[0]))


root = pikli.Command(
    use = "hello",
    short = "test cli app",
    run = greeter
)

serve = pikli.Command(
    use = "serve",
    short = "Starts http server",
    run = start_server
)

serve.flags().intp("port" , "p" , 0 , "the port to start the server")

root.flags().boolp("verbose" , "v" , "shows details")

root.add_command(serve)



root.execute()
