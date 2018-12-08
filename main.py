import pikli


def start_server(cmd , args):
    if pikli.get_bool("important"):
        print("This command is very imporant")
    print("Http server started at {}".format(pikli.get_int("port")))
    if pikli.get_str("config"):
        print("configuration file is at {}".format(pikli.get_str("config")))

root_command = pikli.Command(
        use = "hello",
        short = "Hello is the  first ever cli app made with pikli",
)

serve_command = pikli.Command(
    use = "serve",
    short = "start the http server",
)

migration_command = pikli.Command(
    use = "migrate",
    short = "Runs database migrations",
)



root_command.add_command(serve_command)
root_command.add_command(migration_command)


root_command.persistent_flags().intp("port" , "p" , 2000 , "The Port to do things on")
root_command.flags().stringp("config" , "c" , "" , "Configuration file to read the config from")
root_command.persistent_flags().boolp("important" , "i" , "Determines if important or not")




root_command.execute()
