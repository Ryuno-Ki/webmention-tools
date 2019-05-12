#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from urllib.parse import urljoin, urlsplit, urlunsplit

from bs4 import BeautifulSoup
from httplink import parse_link_header
import requests

import webmentiontools


class WebmentionSend(object):
    def __init__(self, from_url, to_url):
        """
        This class is responsible for sending Webmentions as standardised in
        https://www.w3.org/TR/webmention/#sending-webmentions

        :param from_url: The URL from which to send a Webmention.
        :param to_url: The URL to which to send a Webmention.
        :type from_url: str
        :type to_url: str

        :todo: Read version of requests instead of hardcode it here.
        """
        self.from_url = from_url
        self.to_url = to_url
        self.user_agent = "Webmention Tools/{} requests/{}".format(
            webmentiontools.__version__,
            "2.21.0"
        )

    def check_has_from_url(self):
        """
        Checks, whether the from_url is a valid URL.

        :returns: Is the from_url valid?
        :rtype: bool
        """
        return self._check_valid_url(self.from_url)

    def check_has_to_url(self):
        """
        Checks, whether the to_url is a valid URL.

        :returns: Is the to_url valid?
        :rtype: bool
        """
        return self._check_valid_url(self.to_url)

    def head_url(self):
        """
        Makes a HEAD request to to_url and checks for webmention rel in HTTP
        header.

        :returns: Webmention rel endpoint if found.
        :rtype: str or None
        """
        webmention_link_header = None

        response = requests.head(
            self.to_url,
            allow_redirects=True,
            headers={"User-Agent": self.user_agent}
        )

        if self._is_successful_response(response):
            webmention_link_header = self._get_webmention_link_header(
                response.headers
            )

            if webmention_link_header:
                webmention_link_header = self._ensure_url(webmention_link_header)

        return webmention_link_header

    def get_url(self):
        """
        Makes a GET request to to_url.

        :returns: HTML of endpoint if found.
        :rytpe: str or None
        """
        html = None

        response = requests.get(
            self.to_url,
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
        soup = BeautifulSoup(html, "html.parser")
        links_and_anchors = soup.find_all(["link", "a"])

        webmentions = []
        for link_or_anchor in links_and_anchors:
            if link_or_anchor.attrs.get("rel"):
                if "webmention" in link_or_anchor.attrs.get("rel"):
                    href = link_or_anchor.attrs.get("href")
                    if href is not None:
                        webmention_link = self._ensure_url(href)
                        webmentions.append(webmention_link)

        return webmentions

    def _check_valid_url(self, url_string):
        try:
            result = urlsplit(url_string)
            return all([result.scheme, result.netloc, result.path])
        except:
            return False

    def _is_successful_response(self, response):
        return str(response.status_code).startswith("2")

    def _get_webmention_link_header(self, headers):
        link_header = headers.get("link")
        if link_header is None:
            return None

        parsed = parse_link_header(link_header)
        webmention_link = None
        for link in parsed.links:
            if "webmention" in link.rel:
                webmention_link = link.target
                break

        return webmention_link

    def _ensure_url(self, url_string=""):
        parts = []

        parsed = urlsplit(url_string)
        parsed_to_url = urlsplit(self.to_url)

        if parsed.scheme == "":
            parts.append(parsed_to_url.scheme)
        else:
            parts.append(parsed.scheme)

        if parsed.netloc == "":
            parts.append(parsed_to_url.netloc)
        else:
            parts.append(parsed.netloc)

        if parsed.path == "":
            parts.append(parsed_to_url.path)
        else:
            path = str(parsed.path)
            if path.startswith("/"):
                parts.append(parsed.path)
            else:
                joined_path = urljoin(parsed_to_url.path, parsed.path)
                parts.append(joined_path)

        if parsed.query == "":
            parts.append(parsed_to_url.query)
        else:
            parts.append(parsed.query)

        if parsed.fragment == "":
            parts.append(parsed_to_url.fragment)
        else:
            parts.append(parsed.fragment)

        return str(urlunsplit(tuple(parts)))
