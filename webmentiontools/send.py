#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from urllib.parse import urlparse, urlunparse

from httplink import parse_link_header
import requests


class WebmentionSend(object):
    def __init__(self, from_url, to_url):
        """
        This class is responsible for sending Webmentions as standardised in
        https://www.w3.org/TR/webmention/#sending-webmentions

        :param from_url: The URL from which to send a Webmention.
        :param to_url: The URL to which to send a Webmention.
        :type from_url: str
        :type to_url: str
        """
        self.from_url = from_url
        self.to_url = to_url

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

        response = requests.head(self.to_url)
        if self._is_successful_response(response):
            webmention_link_header = self._get_webmention_link_header(
                response.headers
            )

            webmention_link_header = self._ensure_url(webmention_link_header)

        return webmention_link_header

    def _check_valid_url(self, url_string):
        try:
            result = urlparse(url_string)
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

    def _ensure_url(self, url_string):
        parts = []

        parsed = urlparse(url_string)
        parsed_to_url = urlparse(self.to_url)

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
            parts.append(parsed.path)

        if parsed.params == "":
            parts.append(parsed_to_url.params)
        else:
            parts.append(parsed.params)

        if parsed.query == "":
            parts.append(parsed_to_url.query)
        else:
            parts.append(parsed.query)

        if parsed.fragment == "":
            parts.append(parsed_to_url.fragment)
        else:
            parts.append(parsed.fragment)

        return urlunparse(tuple(parts))
