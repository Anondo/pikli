import sys
import unittest

import pikli

class TestCommand(unittest.TestCase):

    worked = False

    def test_root_command(self):
        """

          Tests that a single command(root) works with the run function

          Command string: <script name>(root)

        """

        def run_func(arg):
            TestCommand.worked = True

        sys.argv = sys.argv[:1]

        root = pikli.Command(use = "root" , short = "the root command" ,
                             run = run_func)


        root.execute()


        self.assertTrue(TestCommand.worked , "Should be true")

        TestCommand.worked = False

    def test_sub_commands(self):
        """

         Tests that the sub commands work with the run function

         Command String: 1.<script name>(root) sub1
                         2.<script name>(root) sub2

        """

        def run_func(arg):
            TestCommand.worked = True

        sys.argv = sys.argv[:1]

        root = pikli.Command(use = "root" , short = "the root command")

        sub1 = pikli.Command(use = "sub1" , short = "the first sub command" ,
                             run = run_func)

        sub2 = pikli.Command(use = "sub2" , short = "the second sub command" ,
                             run = run_func)

        root.add_command(sub1 , sub2)

        sys.argv += ["sub1"]

        root.execute()

        self.assertTrue(TestCommand.worked , "Should be true")

        TestCommand.worked = False

        sys.argv.pop()

        sys.argv += ["sub2"]

        root.execute()

        self.assertTrue(TestCommand.worked , "Should be true")

        TestCommand.worked = False

    def test_multilevel_commands(self):

        """

        Tests that commands/sub-commands on multilevel are working

        Command String: 1.<script name>(root) child
                        2.<script name>(root) child gchild

        """

        def run_func(arg):
            TestCommand.worked = True

        sys.argv = sys.argv[:1]

        root = pikli.Command(use = "root" , short = "The root command")

        child = pikli.Command(use = "child" , short = "The child command" ,
                              run = run_func)

        gchild = pikli.Command(use = "gchild" , short = "The grand child command" ,
                               run = run_func)

        child.add_command(gchild)

        root.add_command(child)

        sys.argv += ["child"]

        root.execute()

        self.assertTrue(TestCommand.worked , "Should be true")

        TestCommand.worked = False

        sys.argv += ["gchild"]

        root.execute()

        self.assertTrue(TestCommand.worked , "Should be true")

        TestCommand.worked = False









if __name__ == "__main__":
    unittest.main()
