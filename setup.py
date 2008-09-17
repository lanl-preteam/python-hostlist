# -*- coding: utf-8 -*-

from distutils.core import setup

setup(name         = "python-hostlist",
      version      = "1.1", # Change in hostlist{,.py}, README, python-hostlist.spec too!
      description  = "Python module for hostlist handling",
      long_description = "The hostlist.py module knows how to expand and collect LLNL hostlist expressions.",
      author       = "Kent Engström",
      author_email = "kent@nsc.liu.se",
      url          = "http://www.nsc.liu.se/~kent/python-hostlist/",
      license      = "GPL2+",
      py_modules   = ["hostlist"],
      scripts      = ["hostlist"],
      )
