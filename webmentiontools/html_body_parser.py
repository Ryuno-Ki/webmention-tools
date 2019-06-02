from urllib.parse import urljoin, urlsplit, urlunsplit

from bs4 import BeautifulSoup


class HtmlBodyParser(object):
    def __init__(self, url):
        """
        Parses the markup for a valid webmention endpoint.

        :param url: The URL to inspect.
        :type url: str
        """
        self.url = url

    def parse(self, markup):
        """
        Searches the markup for a valid webmention endpoint.

        :param markup: The HTML to search through.
        :type markup: str
        :returns: Webmention endpoint if found
        :rtype: str or None
        """
        soup = BeautifulSoup(markup, "html.parser")
        links_and_anchors = soup.find_all(["link", "a"])

        webmentions = []
        for link_or_anchor in links_and_anchors:
            if link_or_anchor.attrs.get("rel"):
                if "webmention" in link_or_anchor.attrs.get("rel"):
                    href = link_or_anchor.attrs.get("href")
                    if href is not None:
                        webmention_link = self._ensure_url(href)
                        webmentions.append(webmention_link)

        if len(webmentions) == 0:
            return None

        return webmentions[0]

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
