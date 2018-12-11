import pikli


def start_server(cmd , args):
    if pikli.get_bool("verbose"):
        print("Showing details")
    print("Server starting at: {}".format(pikli.get_int("port")))


root = pikli.Command(
    use = "hello",
    short = "test cli app"
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
