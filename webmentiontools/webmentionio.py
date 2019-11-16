#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Provides interface to interact with https://webmention.io/
"""

import json
import requests


class WebmentionIO():
    """
    Wrapper for interacting.

    Example:
    webmention_io_token = None # or set your token.
    wio = WebmentionIO(webmention_io_token)
    ret = wio.links_to_url('http://indiewebcamp.com/webmention')
    if not ret:
        print(wio.error)
    else:
        for l in ret['links']:
            print(l['id'], l['source'], l['verified_date'])
    """
    def __init__(self, access_token=None):
        self.access_token = access_token
        self.api_endpoint = 'https://webmention.io/api'
        self.error = None

    def api_links_req(self, key, value):
        """
        Queries API for WebMentions
        """
        if key not in (None, 'target', 'domain'):
            return False
        url = "%s/links" % self.api_endpoint
        headers = {'Accept': 'application/json'}
        payload = {key: value, 'access_token': self.access_token}
        response = requests.get(url, headers=headers, params=payload)
        if response.status_code != 200:
            self.error = response.text
            return False
        return json.loads(response.text)

    def links_to_url(self, url):
        """
        Queries API for results with the given target
        """
        links = self.api_links_req('target', url)
        if not links:
            return False
        return links

    def links_to_domain(self, domain):
        """
        Queries API for results with the given domain
        """
        links = self.api_links_req('domain', domain)
        if not links:
            return False
        return links
