Pikli: Library For CLI Apps
==================

[![License](https://img.shields.io/dub/l/vibe-d.svg)](https://github.com/Anondo/pikli/blob/master/LICENSE)
[![Project status](https://img.shields.io/badge/version-1.0-green.svg)](https://github.com/Anondo/pikli/releases)

A simple python library to build command-line interfaces. Very heavily inspired by [Cobra](https://github.com/spf13/cobra.git)

## Installing

```
pip install pikli
```

## Usage

```python

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
