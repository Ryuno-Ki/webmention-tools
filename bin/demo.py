#!/usr/bin/env python
# -*- coding: utf-8 -*-

from webmentiontools.urlinfo import UrlInfo
from webmentiontools.webmentionio import WebmentionIO

# If you have an access token from webmention.io,
# set it here. Some calls require it.

webmention_io_token = None 

wio = WebmentionIO(webmention_io_token)

# Get all links "mentioning" http://indiewebcamp.com/webmention
target_url = 'http://indiewebcamp.com/webmention'
ret = wio.linksToURL(target_url)

if not ret:
    print wio.error
else:
    for link in ret['links']:
        print 
        print 'Webmention.io ID: %s' % link['id']
        print '    Source: %s' % link['source']
        print '    Verification Date: %s' % link['verified_date']
        
        # Now use UrlInfo to get some more information about the source.
        # Most web apps showing webmentions, will probably do something 
        # like this.
        info = UrlInfo(link['source'])
        print '    Source URL info:'
        print '        Title: %s' % info.title()
        print '        Pub Date: %s' % info.pubDate()
        print '        in-reply-to: %s' % info.inReplyTo()
        print '        Author image: %s' % info.image()
        print '        Snippet: %s' % info.snippetWithLink(target_url)
