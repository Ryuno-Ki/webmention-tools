webmention-tools
===============

Some simple tools in python to deal with webmentions.



Currently: 

- webmentiontools.send implements WebmentionSend 
that sends webmentions.
- webmentiontools.urlinfo implements UrlInfo() that
will rerurn usefull information about a web page, like 
title, the existance of an "in-reply-to" link,
the author name, the author image, etc.
- webmentiontoold.webmentionio provides a class to query
webmention.io

There is also the corresponting command line tool, 
webmention-tools (which is also a simple example on how 
to use the library.

Check bin/demp.py on how to use the library to query 
webmention.io and present information for all URLs that
mentioned http://indiewebcamp.com/webmention


Installation
============

pip install webmentiontools

Usage: 
========

Command line:

    webmention-tools send `source` `target`
    webmention-tools urlinfo `url`

or

Python code to send a webmention:

    from webmentiontools.send import WebmentionSend
    source = 'URL of page sending the webmention'
    target = 'URL of page to receive the webmention'
    mention = WebmentionSend(source, target)
    mention.send()

Python code to get info about a webpage.

    from webmentiontools.urlinfo import UrlInfo
    url = 'a link to a web page'
    i = UrlInfo(url)
    if i.error:
        print 'There was an error getting %s' % url
    else:
        print 'in-reply-to link: %s' % i.inReplyTo()
        print 'publication date: %s' % i.pubDate()
        print 'page title: %s' % i.title()
        print 'image link: %s' % i.image()

