"""

  Pikli CLI Library
  ~~~~~~~~~~~~~~~~~

  Copyright @2018 Ahmad Anondo.  All rights reserved.
  Use of this source code is governed by a MIT-style
  license that can be found in the LICENSE file.

  Pikli is a library , written in python to creat cli interface based apps.

  usage:

        >>> import pikli
        >>> root_command = pikli.Command(
        ...     use = "hello",
        ...     short = "hello is the first ever cli app built using pikli"
        ... )
        >>> root_command.execute()
        hello is the first ever cli app built using pikli



"""





from . command import Command
