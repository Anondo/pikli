import pikli

def run_func(arg):
    print("yolo")

def test(arg):
    print("Hello " , arg[0])

root = pikli.Command(use = "root" , short = "root command" , run = test)

child = pikli.Command(use = "child" , short = "child command" , run = run_func)

child2 = pikli.Command(use = "child2" , short = "child2 command")

root.add_command(child)
root.add_command(child2)

root.execute()
