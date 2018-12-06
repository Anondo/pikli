import pikli


def start_server(cmd , args):
    print("Hello {}".format(args[cmd.arg_pos]))
    print("Http server started at {}".format(pikli.get_int("port")))
    print("yoyo happening with {}".format(pikli.get_int("yo")))

root_command = pikli.Command(
        use = "hello",
        short = "Hello is the  first ever cli app made with pikli",
)

serve_command = pikli.Command(
    use = "serve",
    short = "start the http server",
    run = start_server
)
serve_command.flags().intp("port" , "p" , 2000 , "The Port to do things on")
serve_command.flags().intp("yo" , "y" , 20 , "To do yoyo")

root_command.add_command(serve_command)


root_command.execute()
