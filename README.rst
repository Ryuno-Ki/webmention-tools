webmention-tools
================

|CircleCI| |Vulnerabilities| |Coverage| |Maintainability|

Some simple tools in python to deal with webmentions.

Note, that this package was formerly known as
`webmentiontools <https://pypi.org/project/webmentiontools/>`__, but had
to be renamed due to
`PEP-541 <https://www.python.org/dev/peps/pep-0541/>`__. (Namely, not
classified as abandoned project, because the author was reachable).

Currently:

-  webmentiontools.send implements WebmentionSend that sends
   webmentions.
-  webmentiontools.urlinfo implements UrlInfo() that will rerurn usefull
   information about a web page, like title, the existance of an
   "in-reply-to" link, the author name, the author image, etc.
-  webmentiontoold.webmentionio provides a class to query webmention.io

There is also the corresponting command line tool, webmention-tools
(which is also a simple example on how to use the library.

Check `bin/demo.py <./bin/demo.py>`__ on how to use the library to query
webmention.io and present information for all URLs that mentioned
http://indiewebcamp.com/webmention

Installation
============

pip install webmention-tools

Usage
=====

Command line:

::

    webmention-tools send `source` `target`
    webmention-tools urlinfo `url`

or

Python code to send a webmention:

::

    from webmentiontools.send import WebmentionSend
    source = 'URL of page sending the webmention'
    target = 'URL of page to receive the webmention'
    mention = WebmentionSend(source, target)
    mention.send()

Python code to get info about a webpage.

::

    from webmentiontools.urlinfo import UrlInfo
    url = 'a link to a web page'
    i = UrlInfo(url)
    if i.error:
        print('There was an error getting %s' % url)
    else:
        print('in-reply-to link: %s' % i.inReplyTo())
        print('publication date: %s' % i.pubDate())
        print('page title: %s' % i.title())
        print('image link: %s' % i.image())

Development
===========

1. Create a virtualenv with python3
2. Change into that directory and clone the repository
3. Activate the virtualenv by ``source``\ ing ``bin/activate``
4. Change into the cloned repository and install dependencies via \`pip
   install -r requirements.txt'
5. Run ``pytest --cov`` for unit tests with code coverage

.. |CircleCI| image:: https://circleci.com/gh/Ryuno-Ki/webmention-tools.svg?style=svg
   :target: https://circleci.com/gh/Ryuno-Ki/webmention-tools
.. |Vulnerabilities| image:: https://img.shields.io/snyk/vulnerabilities/github/Ryuno-Ki/webmention-tools.svg?style=popout
.. |Coverage| image:: https://codecov.io/gh/Ryuno-Ki/webmention-tools/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/Ryuno-Ki/webmention-tools
.. |Maintainability| image:: https://api.codeclimate.com/v1/badges/bb63f7d3f38456ea8770/maintainability
   :target: https://codeclimate.com/github/Ryuno-Ki/webmention-tools/maintainability
