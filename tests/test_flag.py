import sys
import unittest

import pikli

class TestFlag(unittest.TestCase):

    def test_bool_flags(self):
        """

        Tests that the bool flags of a/the command(s) are working

        Command String: <script name>(root) -v serve --http

        """

        def start_server(arg):
            pass


        sys.argv = sys.argv[:1]

        root = pikli.Command(use = "root" , short = "the root command")

        serve = pikli.Command(use = "serve" , short = "starts the server" ,
                              run = start_server)

        root.flags().boolp("verbose" , "v" , "show details of an operation")

        serve.flags().boolp("http" , "h" , "starts the http server")

        serve.flags().boolp("grpc" , "g" , "starts the gRPC server")

        root.add_command(serve)

        sys.argv += ["-v" , "serve" , "--http"]

        root.execute()


        verbose = pikli.get_bool("verbose")
        http = pikli.get_bool("http")
        grpc = pikli.get_bool("grpc")

        self.assertTrue(verbose , "Verbose Should be true")
        self.assertTrue(http , "http should be true")
        self.assertFalse(grpc , "grpc shoud be false")

    def test_int_flags(self):
        """

        Tests that the int flags of a/the command(s) are working

        Command String: <script name>(root) -y 2019 serve --port=8080 -w 20

        """

        def start_server(arg):
            pass


        sys.argv = sys.argv[:1]

        root = pikli.Command(use = "root" , short = "the root command")

        serve = pikli.Command(use = "serve" , short = "starts the server" ,
                              run = start_server)

        root.flags().intp("year" , "y" , 2018,  "the current year")

        serve.flags().intp("port" , "p" , 8000  , "the port to run the http server")

        serve.flags().intp("worker" , "w" , 10 ,"number of workers")

        serve.flags().intp("nothing" , "n" , 420 , "flag to test the default value")

        root.add_command(serve)

        sys.argv += ["-y" , "2019" , "serve" , "--port=8080" , "-w" , "20"]

        root.execute()


        year = pikli.get_int("year")
        port = pikli.get_int("port")
        worker = pikli.get_int("worker")
        nothing = pikli.get_int("nothing")

        want_year = 2019
        want_port = 8080
        want_worker = 20
        want_nothing = 420

        self.assertEqual(year , want_year , "Year: Want {} Got {}".format(want_year , year))
        self.assertEqual(port , want_port , "Port: Want {} Got {}".format(want_port , port))
        self.assertEqual(worker , want_worker , "Worker: Want {} Got {}".format(want_worker , worker))
        self.assertEqual(nothing , want_nothing , "Nothing: Want {} Got {}".format(want_nothing , nothing))

    def test_string_flags(self):
       """

       Tests that the string flags of a/the command(s) are working

       Command String: <script name>(root) -n Johnny assign --designation="Software Engineer"
                                           -s "active"

       """

       def run_func(arg):
           pass


       sys.argv = sys.argv[:1]

       root = pikli.Command(use = "root" , short = "the root command")

       assign = pikli.Command(use = "assign" , short = "assigns the employee" ,
                             run = run_func)

       root.flags().stringp("name" , "n" , "A man has no name",  "Name of the employee")

       assign.flags().stringp("designation" , "d" , "killer"  , "Designation of the employee")

       assign.flags().stringp("status" , "s" , "inactive" ,"current status of the employee")

       assign.flags().stringp("nothing" , "n" , "nothing" , "flag to test the default value")

       root.add_command(assign)

       sys.argv += ["-n" , "Johnny" , "assign" , "--designation=Software Engineer" , "-s" , "active"]

       root.execute()


       name = pikli.get_str("name")
       designation = pikli.get_str("designation")
       status = pikli.get_str("status")
       nothing = pikli.get_str("nothing")

       want_name = "Johnny"
       want_designation = "Software Engineer"
       want_status = "active"
       want_nothing = "nothing"

       self.assertEqual(name , want_name , "name: Want {} Got {}".format(want_name , name))
       self.assertEqual(designation , want_designation , "designation: Want {} Got {}".format(want_designation , designation))
       self.assertEqual(status , want_status , "status: Want {} Got {}".format(want_status , status))
       self.assertEqual(nothing , want_nothing , "Nothing: Want {} Got {}".format(want_nothing , nothing))





if __name__ == "__main__":
    unittest.main()
