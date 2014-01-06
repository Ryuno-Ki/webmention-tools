#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urlparse
import requests
from bs4 import BeautifulSoup

class WebmentionSend():

    def __init__(self, source, target):
        self.source_url = source
        self.target_url = target
        self.receiver_endpoint = None

    def send(self, **kwargs):
        self.error = None
        self.requests_kwargs = kwargs
        r = self._discoverEndpoint()
        if not r:
            return False
        return self._notifyReceiver()

    def _discoverEndpoint(self):
        r = requests.get(self.target_url, **self.requests_kwargs)
        if r.status_code != 200:
            self.error = {
                'code':'BAD_TARGET_URL',
                'error_description': 'Unable to get target URL.',
                'request': 'GET %s' % self.target_url,
                'http_status': r.status_code,
            }
            return False
        html = r.text
        soup = BeautifulSoup(html)
        tag = soup.find('link', attrs={'rel': 'webmention'})
        if not tag:
            # backward compatibility with the webmention 0.1 spec
            tag = soup.find('link', attrs={'rel': 'http://webmention.org/'})

        if tag and tag['href']:
            # add the base scheme and host to relative endpoints
            self.receiver_endpoint = urlparse.urljoin(self.target_url, tag['href'])
            return True
        else:
            self.error = {
                'code': 'NO_ENDPOINT',
                'error_description': 'Unable to discover webmention endpoint.'
            }
            return False

    def _notifyReceiver(self):
        payload = {'source': self.source_url, 'target': self.target_url}
        headers = {'Accept': '*/*'}
        r = requests.post(self.receiver_endpoint, data=payload, **self.requests_kwargs)

        request_str = 'POST %s (with source=%s, target=%s)' % (self.receiver_endpoint, self.source_url, self.target_url)
        if r.status_code / 100 != 2:
            self.error = {
                'code':'RECEIVER_ERROR',
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
