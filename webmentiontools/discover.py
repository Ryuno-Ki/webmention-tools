#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from urllib.parse import urlsplit

import requests

import webmentiontools
from .html_body_parser import HtmlBodyParser
from .http_header_parser import HttpHeaderParser


class WebmentionDiscover(object):
    def __init__(self,
                 url,
                 html_body_parser=None,
                 http_header_parser=None):
        """
        This class is responsible for sending Webmentions as standardised in
        https://www.w3.org/TR/webmention/#sending-webmentions

        :param url: The URL to which to send a Webmention.
        :param html_body_parser: A class implementing HtmlBodyParser interface.
        :param http_header_parser: A class implementing HttpHeaderParser
        interface.
        :type url: str
        """
        self.url = url

        if html_body_parser is not None:
            self.html_body_parser = html_body_parser(url)
        else:
            self.html_body_parser = HtmlBodyParser(url)

        if http_header_parser is not None:
            self.http_header_parser = http_header_parser(url)
        else:
            self.http_header_parser = HttpHeaderParser(url)

        self.user_agent = "Webmention Tools/{} requests/{}".format(
            webmentiontools.__version__,
            requests.__version__
        )

    def check_has_url(self):
        """
        Checks, whether the url is a valid URL.

        :returns: Is the url valid?
        :rtype: bool
        """
        return self._check_valid_url(self.url)

    def head_url(self):
        """
        Makes a HEAD request to url and checks for webmention rel in HTTP
        header.

        :returns: Webmention rel endpoint if found.
        :rtype: str or None
        """
        return self.http_header_parser.parse()

    def get_url(self):
        """
        Makes a GET request to url.

        :returns: HTML of endpoint if found.
        :rytpe: str or None
        """
        html = None

        response = requests.get(
            self.url,
            allow_redirects=True,
            headers={"User-Agent": self.user_agent}
        )
        if self._is_successful_response(response):
            if response.headers.get("content-type").startswith("text/html"):
                html = response.text

        return html

    def find_webmention_links(self, html):
        """
        Searches the HTML for all <link> and <a> tags outside of comments.
        Filter them for rel="webmention".

        :param html: The HTML to search through.
        :type html: str
        :returns: List of URLs which are webmentions.
        :rtype: list(str)
        """
        return self.html_body_parser.parse(html)

    def _check_valid_url(self, url_string):
        try:
            result = urlsplit(url_string)
            return all([result.scheme, result.netloc, result.path])
        except Exception:
            return False

    def _is_successful_response(self, response):
        return str(response.status_code).startswith("2")
