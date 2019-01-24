#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import itertools
import re
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup


class WebmentionSend():

    LINK_HEADER_RE = re.compile(
        r'''<([^>]+)>; rel=["'](https://)?webmention(\.org/?)?["']''')

    def __init__(self, source, target, endpoint=None):
        self.source_url = source
        self.target_url = target
        self.receiver_endpoint = endpoint

    def send(self, **kwargs):
        self.error = None
        self.requests_kwargs = kwargs
        if not self.receiver_endpoint:
            self._discoverEndpoint()
        if not self.receiver_endpoint:
            return False
        return self._notifyReceiver()

    def _discoverEndpoint(self):
        r = requests.get(self.target_url, verify=False, **self.requests_kwargs)
        if r.status_code != 200:
            self.error = {
                'code': 'BAD_TARGET_URL',
                'error_description': 'Unable to get target URL.',
                'request': 'GET %s' % self.target_url,
                'http_status': r.status_code,
            }
            return
        self.html = r.text

        # look in the headers
        # XXX: it looks like requests doesn't handle multiple headers with the
        # same name, e.g. 'Link'. from skimming the code, it looks like the last
        # one wins. ugh. :/
        for link in r.headers.get('link', '').split(','):
            match = self.LINK_HEADER_RE.search(link)
            if match:
                self.receiver_endpoint = urljoin(self.target_url,
                                                 match.group(1))
                return

        # look in the content
        soup = BeautifulSoup(self.html, 'html.parser')
        tag = None
        for name, rel in itertools.product(
            ('link', 'a'), ('webmention', 'https://webmention.org/')
        ):
            tag = soup.find(name, attrs={'rel': rel})
            if tag:
                break

        if tag and tag.get('href'):
            # add the base scheme and host to relative endpoints
            self.receiver_endpoint = urljoin(
                self.target_url, tag['href']
            )
        else:
            self.error = {
                'code': 'NO_ENDPOINT',
                'error_description': 'Unable to discover webmention endpoint.'
            }

    def _notifyReceiver(self):
        payload = {'source': self.source_url, 'target': self.target_url}
        r = requests.post(
            self.receiver_endpoint,
            verify=False,
            data=payload,
            **self.requests_kwargs
        )

        request_str = 'POST %s (with source=%s, target=%s)' % (
            self.receiver_endpoint,
            self.source_url,
            self.target_url
        )
        if r.status_code / 100 != 2:
            self.error = {
                'code': 'RECEIVER_ERROR',
                'request': request_str,
                'http_status': r.status_code,
                }
            try:
                self.error.update(r.json())
            except:
                self.error['body'] = r.text
            return False
        else:
            self.response = {
                'request': request_str,
                'http_status': r.status_code,
                'body': r.text
            }
            return True

if __name__ == '__main__':
    pass
