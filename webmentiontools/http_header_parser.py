from urllib.parse import urljoin, urlsplit, urlunsplit

from httplink import parse_link_header
import requests

import webmentiontools


class HttpHeaderParser(object):
    def __init__(self, url):
        """
        This class parses the HTTP header for the given URL for webmention
        relationships.

        :param url: The URL to inspect.
        :type url: str
        """
        self.url = url
        self.user_agent = "Webmention Tools/{} requests/{}".format(
            webmentiontools.__version__,
            requests.__version__
        )

    def parse(self):
        """
        Make a HEAD request and check for webmention rol in HTTP header.

        :returns: Webmention rel endpoint if found.
        :rtype: str or None
        """
        webmention_endpoint = None

        response = requests.head(
            self.url,
            allow_redirects=True,
            headers={"User-Agent": self.user_agent}
        )

        if self._is_successful_response(response):
            webmention_endpoint = self._get_webmention_endpoint(
                response.headers
            )

            if webmention_endpoint:
                webmention_endpoint = self._ensure_url(webmention_endpoint)

        return webmention_endpoint

    def _is_successful_response(self, response):
        return str(response.status_code).startswith("2")

    def _get_webmention_endpoint(self, headers):
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
        parsed_url = urlsplit(self.url)

        if parsed.scheme == "":
            parts.append(parsed_url.scheme)
        else:
            parts.append(parsed.scheme)

        if parsed.netloc == "":
            parts.append(parsed_url.netloc)
        else:
            parts.append(parsed.netloc)

        if parsed.path == "":
            parts.append(parsed_url.path)
        else:
            path = str(parsed.path)
            if path.startswith("/"):
                parts.append(parsed.path)
            else:
                joined_path = urljoin(parsed_url.path, parsed.path)
                parts.append(joined_path)

        if parsed.query == "":
            parts.append(parsed_url.query)
        else:
            parts.append(parsed.query)

        if parsed.fragment == "":
            parts.append(parsed_url.fragment)
        else:
            parts.append(parsed.fragment)

        return str(urlunsplit(tuple(parts)))
