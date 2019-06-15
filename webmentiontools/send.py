#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from webmentiontools.discover import WebmentionDiscover
from webmentiontools.request import request_post_url


class WebmentionSend(object):
    def __init__(self, from_url, to_url):
        self.from_url = from_url
        self.to_url = to_url
        self.discover = WebmentionDiscover(to_url)

    def send_notification(self):
        """
        Sends a notification to the target server to trigger a webmention
        comment.

        :returns: Was notification successful?
        :rtype: bool
        """
        endpoint = self.discover.discover()

        if endpoint is None:
            return False

        VALID_STATUS_CODES = (201, 202)
        ACCEPTED_STATUS_CODES = (200, )
        STATUS_CODES = VALID_STATUS_CODES + ACCEPTED_STATUS_CODES

        response = request_post_url(endpoint, self.from_url, self.to_url)
        if int(response.status_code) in STATUS_CODES:
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
