import pikli

def greet(args):
    print("Hello {}, beef cheese delight rocks".format(args[0]))

root = pikli.Command(use = "hello" , short = "hello is a greeting app",
                     run = greet)

root.execute()
