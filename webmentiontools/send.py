#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests

import webmentiontools


class WebmentionSend(object):
    def __init__(self, from_url, to_url, discover = None):
        self.user_agent = "Webmention Tools/{} requests/{}".format(
            webmentiontools.__version__,
            "2.21.0"
        )
        self.from_url = from_url
        self.to_url = to_url

        if discover is None:
            self.discover = WebmentionDiscover(from_url, to_url)
        else:
            self.discover = discover(from_url, to_url)

    def send_notification(self):
        """
        Sends a notification to the target server to trigger a webmention
        comment.

        :returns: Was notification successful?
        :rtype: bool
        """
        endpoint = self.discover.head_url()

        if endpoint is None:
            html = self.discover.get_url()
            links = self.discover.find_webmention_links(html)
            endpoint = links[0] if len(links) > 0 else None

        if endpoint is None:
            return False

        payload = {"source": self.from_url, "target": self.to_url}
        response = requests.post(
            endpoint,
            data=payload,
            allow_redirects=True,
            headers={"User-Agent": self.user_agent}
        )

        if int(response.status_code) in (200, 201, 202):
            return True

        return False

    def delete_webmention(self):
        """
        Sends a notification to the target server to trigger removal of a
        webmention comment.

        :returns: Was webmention comment successfully removed?
        :rtype: bool
        """
        return self.send_notification()
