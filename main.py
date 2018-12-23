import pikli

def start_server(args):
  print("HTTP server running on port: {}".format(pikli.get_int("port")))

root = pikli.Command(use = "hello" , short = "hello is a cli app")

serve = pikli.Command(use = "serve" , short = "starts the http server",

                      run = start_server
        )

serve.flags().intp("port" , "p" , 8000 , "the port on which the server runs")

root.add_command(serve)

root.execute()
