#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json

class WebmentionIO():
    # Basic library for http://webmention.io/ API

    def __init__(self, access_token=None):
        self.access_token = access_token
        self.api_endpoint = 'http://webmention.io/api'

    def api_links_req(self, k, v):
        if k not in (None, 'target', 'domain'):
            return False
        url = "%s/links" % self.api_endpoint
        headers = {'Accept': 'application/json'}
        payload = { k:v, 'access_token': self.access_token }
        r = requests.get(url, headers=headers, params=payload)       
        if r.status_code != 200:
            self.error = r.text
            return False
        return json.loads(r.text)

    def linksToURL(self, url):
        links = self.api_links_req('target', url)
        if not links:
            return False
        else:
            return links

    def linksToDomain(self, domain):
        links = self.api_links_req('domain', domain)
        if not links:
            return False
        else:
            return links
        
    def linksToAll(self):
        pass

if __name__ == '__main__':
    pass
    """ Example:
    webmention_io_token = None # or set your token.
    wio = WebmentionIO(webmention_io_token)
    ret = wio.linksToURL('http://indiewebcamp.com/webmention')
    if not ret:
        print wio.error
    else:
        for l in ret['links']:
            print l['id'], l['source'], l['verified_date']
    """