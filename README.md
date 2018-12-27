Pikli: Library For Making CLI Apps
==================

[![Build Status](https://travis-ci.org/Anondo/pikli.svg?branch=master)](https://travis-ci.org/Anondo/pikli)
[![License](https://img.shields.io/dub/l/vibe-d.svg)](https://github.com/Anondo/pikli/blob/master/LICENSE)
[![Project status](https://img.shields.io/badge/version-1.0-green.svg)](https://github.com/Anondo/pikli/releases)
[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-370/)

A simple python library to build command-line interfaces. Heavily inspired by [Cobra](https://github.com/spf13/cobra.git).

## Installing

```
pip install pikli
```

## Getting Started

Pikli is a command line parser. It parses the arguments provided on the command prompt & decides whether its a command or a flag or an argument for a command & acts accordingly. A command may have: Flags , Arguments & Sub Commands. In the following example:

```python

#main.py

import pikli

def start_server(arg):
  print("HTTP server running")

root = pikli.Command(use = "hello" , short = "hello is a cli app")

serve = pikli.Command(use = "serve" , short = "starts the http server",

                      run = start_server
        )

root.add_command(serve)

root.execute()



```
We have two commands ```root``` & ```serve```. ```root``` as its name suggests is the root command. This decision is made by providing a parent-child relationship. Its basically a tree like structure. And the command which sits at the top of the tree is the root. The ```serve``` command is made a sub/child command of ```root``` by the ```add_command``` method of the ```Command``` class.The ```add_command``` method takes arbitrary amount of commands to add as a ```sub command```. And ```execute``` does exactly what it looks like, executes the command. Now onto the parameters provided while creating the objects:<br/>
**```use```**: Determines the name of the command. Mandatory.<br/>
**```short```**: A short description of the command.<br/>
**```long```**: A long description of the command.<br/>
**```run```**: The function which is triggered when the ```execute``` method of a command is called. There is a thing to remember about the ```run``` funtion. The function which is to be used as the ```run``` function(in this case **start_server**), **must have a single parameter which will be used as a list.**.

### Flags

Flags are extra options used with a command. For example: ```git commit -m "Initial Commit"``` here, **git** is the **root command**, **commit** is the **sub command**, **-m** is the ``flag`` & the string after that is its value. Now lets see a pikli example:

```python
import pikli

def start_server(arg):
  print("HTTP server running on port: {}".format(pikli.get_int("port")))

root = pikli.Command(use = "hello" , short = "hello is a cli app")

serve = pikli.Command(use = "serve" , short = "starts the http server",

                      run = start_server
        )

serve.flags().intp("port" , "p" , 8000 , "the port on which the server runs")

root.add_command(serve)

root.execute()

```
The ```flags``` method of a ```Command``` returns the ```flag``` object that handles every flag related activity for the command. ```intp``` is a method of that object which creates an ```integer flag```.There is also ```stringp``` & ```boolp```. The first parameter is the name of the flag(used in the long version), the second one is the usable name of the flag like, ```-p```. The third parameter is the default value for the flag. There is no default value for the bool flag. Its False by default. And the fourth one should be obvious, a description of the flag. Now lets use everything we have seen so far:<br/>
```
python main.py serve -p 8080
```
 <br/>

 or

 <br/>

 ```
 python main.py serve --port=8080
 ```
 <br/>
The output should be: <br/>

```
HTTP server running on port: 8080
```
<br/>

Executing the serve command without the ```p``` flag will return the default value when ```pikli.get_int("port")``` is called which is a pikli core function used for retrieving the value of an integer flag. Similarly there are ```get_str``` & ```get_bool``` to get **string** & **bool** flag values.

### The Help Flag

**Pikli** provides an automatic help flag generation & recognition. Whenever a ```command``` without a ```run``` function is executed, the ```help``` flag will be executed autmatically. Or, it can be explicitly mentioned like any other flag like ```-h``` or ```--help```. Try: <br/>
```
python main.py serve --help
```
<br/>

Simply running ```python main.py``` will trigger its help flag as it has no ```run``` function. A help flag should display something similar: <br/>
```
hello is a cli app


Usage:
	hello [args] [flags] [sub commands]


Available Commands:
serve            starts the http server


Flags:
-h, --help                Shows info regarding the command
```

### The Persistent Flag

**Pikli** provides support for ```persistent flags```. ```Persistent flags``` are like normal ```flags``` except if you assign it to a ```command``` it automatically gets assigned to every child it has upto the bottom of the ```command``` tree. So if a ```persistent flag``` is assigned to the ```root command``` then every ```command``` will get that ```flag```. <br/>

```python
import pikli

def start_server(arg):
  if pikli.get_bool("verbose"):
      print("showing details")
  print("HTTP server running on port: {}".format(pikli.get_int("port")))


root = pikli.Command(use = "hello" , short = "hello is a cli app")

serve = pikli.Command(use = "serve" , short = "starts the http server",

                      run = start_server
        )

serve.flags().intp("port" , "p" , 8000 , "the port on which the server runs")

root.add_command(serve)

root.persistent_flags().boolp("verbose" , "v" , "shows details regarding the operation")

root.execute()

```
Here the **verbose** ```flag``` is assigned to the ```root command``` making this flag a global one. When assigning ```persistent flags```, don't forget to add all the ```sub commands``` at first.

### Args

Apart from ```sub commands``` & ```flags``` normal arguments can be used in **pikli**. All that is needed is the ```arg``` list that is used as the parameter of the ```run``` function. Lets see an example:<br/>

```python
import pikli

def greet(arg):
    print("Hello {}, beef cheese delight rocks".format(arg[0]))

root = pikli.Command(use = "hello" , short = "hello is a greeting app",
                     run = greet)

root.persistent_flags().boolp("verbose" , "v" , "shows details regarding the operation")

root.execute()

```
<br/>

Just keep the index order of the ```arguments``` right. The index number of the ```arguments``` doesn't bother about the ```flags```. For example  **``` python main.py -v "John Doe" ```** **pikli** will ignore the flags & count the ```argument``` **John Doe** as index 0 & so on. The output should be: <br/>

```
Hello John Doe, beef cheese delight rocks
```

### Env

Lastly you can get the string or integer environmental variables using **pikli**. The two functions for this are ```get_str_env``` & ```get_int_env```: <br/>

```python
import pikli

def greet(arg):
    print("Hello {}, beef cheese delight rocks".format(pikli.get_str_env("NAME")))

root = pikli.Command(use = "hello" , short = "hello is a greeting app",
                     run = greet)

root.execute()

```

<br/>

Run it like this: <br/>
```
NAME="John Doe" python main.py
```

## Contributing
Totally open to suggestions. [See the contribution guide](https://github.com/Anondo/pikli/blob/master/CONTRIBUTING.md)

## License

Pikli is licensed under the [MIT License](https://github.com/Anondo/pikli/blob/master/LICENSE)
