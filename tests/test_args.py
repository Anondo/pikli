import sys
import unittest

import pikli

class TestArgs(unittest.TestCase):

    fname = ""
    lname = ""

    def test_args(self):

        """

        Tests that the arguments provided with the commands are properly parsed
        among the flags

        Command String: <script name>(root) John -p 8080 Doe --worker=20 child

        """

        def run_func(arg):
            TestArgs.fname = arg[0]
            TestArgs.lname = arg[1]

        def no_func(arg):
            pass

        sys.argv = sys.argv[:1]

        root = pikli.Command(use = "root" , short = "the root command",
                             run = run_func)
        child = pikli.Command(use = "child" , short = "the child command",
                              run = no_func)

        root.flags().intp("port" , "p" , 8000 , "the port")
        root.flags().intp("worker" , "w" , 10 , "the workers")

        sys.argv += ["John" , "-p" , "8080" , "Doe" , "--worker=20" , "child"]

        root.execute()

        got = TestArgs.fname + " " + TestArgs.lname

        want = "John Doe"

        self.assertEqual(got , want , "{} should have been {}".format(got , want))

        port = pikli.get_int("port")
        worker = pikli.get_int("worker")

        self.assertEqual(port , 8080 , "Should have been 8080")
        self.assertEqual(worker , 20 , "Should have been 20")
