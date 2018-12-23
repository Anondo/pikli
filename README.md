Pikli: Library For CLI Apps
==================

[![License](https://img.shields.io/dub/l/vibe-d.svg)](https://github.com/Anondo/pikli/blob/master/LICENSE)
[![Project status](https://img.shields.io/badge/version-1.0-green.svg)](https://github.com/Anondo/pikli/releases)

A simple python library to build command-line interfaces. Very heavily inspired by [Cobra](https://github.com/spf13/cobra.git).

## Installing

```
pip install pikli
```

## Usage

Pikli is a command line parser. It parses the arguments provided on the command prompt & decides whether its a command or a flag or an argument for a command & acts accordingly. A command may have: Flags , Arguments & Sub Commands. In the following example:

```python

#main.py

import pikli

def start_server(args):
  print("HTTP server running")

root = pikli.Command(use = "hello" , short = "hello is a cli app")

serve = pikli.Command(use = "serve" , short = "starts the http server",

                      run = start_server
        )

root.add_command(serve)

root.execute()



```
We have two commands ```root``` & ```serve```. ```root``` as its name suggests is the root command. This decision is made by providing a parent-child relationship. Its basically a tree like structure. And the commands which sits at the top of the tree is the root. The ```serve``` command is made a sub/child command of ```root``` by the ```add_command``` method of the ```Command``` class. And ```execute``` does exactly what it looks like, executes the command. Now onto the parameters provided while creating the objects:<br/>
**```use```**: Determines the name of the command. Mandatory.<br/>
**```short```**: A short description of the command.<br/>
**```long```**: A long description of the command.<br/>
**```run```**: The function which is triggered when the ```execute``` method of a command is called. There is a thing to remember about the ```run``` funtion. The function which is to be used as the ```run``` function(in this case **start_server**), **must have a single parameter which will be used as a list under the hood**.

### Flags

Flags are extra options used with a command. For example: ```git commit -m "Initial Commit"``` here, **git** is the **root command**, **commit** is the **sub command**, **-m** is the ``flag`` & the string after that is its value. Now lets see a pikli example:

```python
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

```
The ```flags``` method of a ```Command``` returns the ```flag``` object that handles every flag related activity for the command. ```intp``` is a method of that object which creates an ```integer flag```.There is also ```stringp``` & ```boolp```. The first parameter is the name of the flag(used in the long version), the one is the usable name of the flag like, ```-p```. The third parameter is the default value for the flag. There is no default value for the bool flag. Its False by default. And the fourth one should be obvious, a description of the flag. Now lets use everything we have seen so far:<br/>
```
python main.py serve -p 8080
```
 <br/>
The output should be: <br/>
```
HTTP server running on port: 8080
```
<br/>
Executing the serve flag without the ```p``` flag will return the default value when ```pikli.get_int("port")``` is called which is a pikli core function used for retrieving the value of an integer flag. Similarly there are ```get_str``` & ```get_bool``` to get **string** & **bool** flag values.

### The Help Flag

### The Persistent Flag

### Args
