webmention-tools
===============

Some simple tools in python to deal with webmentions.

Currently, webmentiontools.send implements WebmentionSend 
that sends webmentions.

There is also the corresponting command line tool, 
webmention-send.py (which is also a simple example on how 
to use the library.


Installation
============

pip install webmention-tools

Usage: 
========

webmention-send.py source target

or

    from webmentiontools.send import WebmentionSend
    mention = WebmentionSend(source, target)
    mention.send()
