import pikli



def start_server(args):
    if pikli.get_bool("verbose"):
        print("Showing details")
    print("server running at http://localhost:{}".format(pikli.get_int("port")))

def up(args):
    print("Database populated successfully")

def down(args):
    print("Database depopulated successfully")



root_command = pikli.Command(
    use = "hello",
    short = "Root command of all the available commands"
)

serve_command = pikli.Command(
    use = "serve",
    short = "Starts the http server at the given port",
    run = start_server
)
serve_command.flags().intp("port" , "p" , 8000 , "the port to run the http server on")

migration_command = pikli.Command(
    use = "migration",
    short = "Runs database migrations"
)
up_command = pikli.Command(
    use = "up",
    short = "Populates the database",
    run = up
)
down_command = pikli.Command(
    use = "down",
    short = "Depopulates the database",
    run = down
)
migration_command.add_command(up_command)
migration_command.add_command(down_command)

root_command.add_command(serve_command)
root_command.add_command(migration_command)

root_command.flags().boolp("verbose" , "v" , "shows details")

root_command.execute()
