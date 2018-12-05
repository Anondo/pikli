import sys
import pikli


def up_database(cmd , args):
    print("Database Populated")
def down_database(cmd , args):
    print("Database Depopulated")

root_command = pikli.Command(
        use = "hello",
        short = "Hello is the  first ever cli app made with pikli",
)

migration_command = pikli.Command(
        use = "migration",
        short = "Runs Database migrations"
)
up_command = pikli.Command(
    use = "up",
    short = "populates the database",
    run = up_database
)
down_command = pikli.Command(
    use = "down",
    short = "depopulates the database",
    run = down_database
)

migration_command.add_command(up_command)
migration_command.add_command(down_command)

root_command.add_command(migration_command)


root_command.execute()
