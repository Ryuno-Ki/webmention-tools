try:
    from urllib.parse import urljoin, urlsplit, urlunsplit
except ImportError:  # Python2.7
    from urlparse import urljoin, urlsplit, urlunsplit

from bs4 import BeautifulSoup
try:
    from httplink import parse_link_header
except (ImportError, SyntaxError):  # Python 2.7
    from httplink.backport import parse_link_header


def parse_headers(target_url, headers):
    """
    Searches the headers for a valid Webmention endpoint.

    :param target_url: The URL from which the headers are passed.
    :param headers: The headers to search through.
    :type target_url: str
    :type headers: dict
    :returns: Webmention endpoint if found
    :rtype: str or None
    """
    case_insensitive_headers = _make_case_insensitive(headers)
    link_header = case_insensitive_headers.get("link")
    if link_header is None:
        return None

    parsed = parse_link_header(link_header)
    webmention_link = None
    for link in parsed.links:
        if "webmention" in link.rel:
            webmention_link = _ensure_url(target_url, link.target)
            break

    return webmention_link


def parse_html(target_url, html):
    """
    Searches the markup for a valid Webmention endpoint.

    :param target_url: The URL from which the HTML is passed.
    :param html: The HTML to search through.
    :type target_url: str
    :type html: str
    :returns: Webmention endpoint if found
    :rtype: str or None
    """
    soup = BeautifulSoup(html, "html.parser")
    links_and_anchors = soup.find_all(["link", "a"])

    webmentions = []
    for link_or_anchor in links_and_anchors:
        if link_or_anchor.attrs.get("rel"):
            if "webmention" in link_or_anchor.attrs.get("rel"):
                href = link_or_anchor.attrs.get("href")
                if href is not None:
                    webmention_link = _ensure_url(target_url, href)
                    webmentions.append(webmention_link)

    if len(webmentions) == 0:
        return None

    return webmentions[0]


def _make_case_insensitive(case_sensitive_dict):
    result = {}
    for item in case_sensitive_dict.items():
        key = item[0].lower()
        value = item[1]
        result[key] = value
    return result


def _ensure_url(target_url, url_string=""):
    parts = []

    parsed = urlsplit(url_string)
    parsed_url = urlsplit(target_url)

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
