import unittest

from webmentiontools.parser import parse_headers, parse_html

from .endpoints import WEBMENTION_ROCKS_TESTS


class ParserTestCase(unittest.TestCase):
    def test_parse_headers(self):
        for test in WEBMENTION_ROCKS_TESTS:
            if test["source"] == "header":
                endpoint = parse_headers(test["url"], test["headers"])
                assert endpoint == test["endpoint"]

    def test_parse_html(self):
        for test in WEBMENTION_ROCKS_TESTS:
            if test["source"] == "html":
                endpoint = parse_html(test["url"], test["html"])
                assert endpoint == test["endpoint"]
