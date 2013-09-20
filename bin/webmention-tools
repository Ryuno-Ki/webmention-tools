#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Usage:
  webmention-send.py [options] <source> <target> 
  webmention-send.py -h, --help
  webmention-send.py --version

Options:
    --debug   	Show error messages [default: False].

You can also use this as a python library. See source.
"""
from webmentiontools import __version__
from webmentiontools.send import WebmentionSend 
from docopt import docopt
from pprint import pprint

args = docopt(__doc__, version=__version__)

if args['<source>'] and args['<target>']:
    # This is how you can use the library.
    # Just initialize WebmentionSend with source, target and call send().
    # 
    mention = WebmentionSend(source=args['<source>'], target=args['<target>'])
    if mention.send():
        print 'Success!'
    else:
        print 'Failed'
        if args['--debug']:
            pprint(mention.error)
