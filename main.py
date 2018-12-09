import pikli


def start_server(cmd , args):
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

serve.flags().intp("port" , "p" , "asas" , "the port to start the server")

root.add_command(serve)



root.execute()
