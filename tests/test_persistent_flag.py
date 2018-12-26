import sys
import unittest

import pikli


class TestPersistentFlag(unittest.TestCase):


    def test_persistent_bool_flag(self):

        """

        Tests that the persistent bool flags of a/the command(s) are working

        Command String: 1.<script name>(root) -v
                        2.<script name>(root) child -v
                        3.<script name>(root) child gchild -v

        """

        def run_func(arg):
            pass

        sys.argv = sys.argv[:1]

        root = pikli.Command(use = "root" , short = "the root command",
                             run = run_func)

        child = pikli.Command(use = "child" , short = "the child command",
                              run = run_func)

        gchild = pikli.Command(use = "gchild" , short = "the grand child command",
                               run = run_func)

        root.persistent_flags().boolp("verbose" , "v" , "shows details of the operation")


        child.add_command(gchild)

        root.add_command(child)

        sys.argv += ["-v"]

        root.execute()

        verbose = pikli.get_bool("verbose")

        self.assertTrue(verbose , "Verbose should be true")

        sys.argv.pop()
        sys.argv += ["child" , "-v"]

        verbose = pikli.get_bool("verbose")

        self.assertTrue(verbose , "Verbose should be true")

        sys.argv.pop()
        sys.argv += ["gchild" , "-v"]

        verbose = pikli.get_bool("verbose")

        self.assertTrue(verbose , "Verbose should be true")
