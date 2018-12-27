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

    def test_persistent_int_flag(self):

        """

        Tests that the persistent int flags are working

        Command String: 1.<script name>(root) serve --port=8080 http
                        2.<script name>(root) serve http -p 3000

        """


        def run_func(arg):
            pass

        sys.argv = sys.argv[:1]

        root = pikli.Command(use = "root" , short = "this is the root command")

        serve = pikli.Command(use = "serve" , short = "starts the server")

        http = pikli.Command(use = "http" , short = "the http server" ,
                             run = run_func)

        serve.add_command(http)

        serve.persistent_flags().intp("port" , "p" , 8000 , "the port to run the server on")

        root.add_command(serve)

        sys.argv += ["serve" , "--port=8080" , "http"]

        root.execute()

        self.assertEqual(pikli.get_int("port") , 8080 , "Should have been 8080")

        sys.argv = sys.argv[:1]
        sys.argv += ["serve" , "http" , "-p" , "3000"]

        root.execute()

        self.assertEqual(pikli.get_int("port") , 3000 , "Should have been 3000")

    def test_persistent_string_flag(self):

        """

        Tests that the persistent string flags are working

        Command String: 1.<script name>(root) -n Alex
                        2.<script name>(root) child1 --name=Barry
                        3.<script name>(root) child2 -n Kane

        """


        def run_func(arg):
            pass

        sys.argv = sys.argv[:1]

        root = pikli.Command(use = "root" , short = "this is the root command",
                             run = run_func)

        child1 = pikli.Command(use = "child1" , short = "the child1 command",
                               run = run_func)

        child2 = pikli.Command(use = "child2" , short = "the child2 command" ,
                             run = run_func)

        root.add_command(child1)
        root.add_command(child2)

        root.persistent_flags().stringp("name" , "n" , "unamed" , "the name")


        sys.argv += ["-n" , "Alex"]

        root.execute()

        self.assertEqual(pikli.get_str("name") , "Alex" , "Should have been Alex")

        sys.argv = sys.argv[:1]
        sys.argv += ["child1" , "--name=Barry"]

        root.execute()

        self.assertEqual(pikli.get_str("name") , "Barry" , "Should have been Barry")

        sys.argv = sys.argv[:1]
        sys.argv += ["child2" , "-n" , "Kane"]

        root.execute()

        self.assertEqual(pikli.get_str("name") , "Kane" , "Should have been Kane")
