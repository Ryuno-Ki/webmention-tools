#!/usr/bin/env python3
# -*- coding: utf-8 -*-
try:
    from urllib.parse import urlsplit
except ImportError:  # Python2.7
    from urlparse import urlsplit

from webmentiontools.parser import parse_headers, parse_html
from webmentiontools.request import (
    is_successful_response,
    request_get_url,
    request_head_url
)


class WebmentionDiscover(object):
    def __init__(self, url):
        """
        This class is responsible for sending Webmentions as standardised in
        https://www.w3.org/TR/webmention/#sending-webmentions

        :param url: The URL to which to send a Webmention.
        :type url: str
        """
        self.url = url

    def check_has_url(self):
        """
        Checks, whether the url is a valid URL.

        :returns: Is the url valid?
        :rtype: bool
        """
        return self._check_valid_url(self.url)

    def discover(self):
        """
        Discovers the endpoint.

        :returns: Webmention endpoint if found.
        :rtype: str or None
        """
        webmention_in_headers = self._head_url()
        if webmention_in_headers is not None:
            return webmention_in_headers

        webmention_in_html = self._get_url()
        if webmention_in_html is not None:
            return webmention_in_html

        return None

    def _head_url(self):
        """
        Makes a HEAD request to url and checks for webmention rel in HTTP
        header.

        :returns: Webmention rel endpoint if found.
        :rtype: str or None
        """
        webmention = None
        response = request_head_url(self.url)
        if is_successful_response(response):
            headers = dict(response.headers)
            webmention = parse_headers(self.url, headers)

        return webmention

    def _get_url(self):
        """
        Makes a GET request to url and checks for webmention in HTML.

        :returns: Webmention rel endpoint if found.
        :rytpe: str or None
        """
        webmention = None
        response = request_get_url(self.url)
        if is_successful_response(response):
            html = response.text
            webmention = parse_html(self.url, html)

        return webmention

    def _check_valid_url(self, url_string):
        result = urlsplit(url_string)
        return all([result.scheme, result.netloc, result.path])
