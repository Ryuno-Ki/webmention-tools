import unittest

from webmentiontools.html_body_parser import HtmlBodyParser

from .endpoints import WEBMENTION_ROCKS_TESTS

MOCK_URL_WITHOUT_HEADER = WEBMENTION_ROCKS_TESTS[2]["test"]


class HtmlBodyParserTestCase(unittest.TestCase):
    def test_init(self):
        html_body_parser = HtmlBodyParser(MOCK_URL_WITHOUT_HEADER)
        assert html_body_parser.url == MOCK_URL_WITHOUT_HEADER

    def test_parse(self):
        html_body_parser = HtmlBodyParser()
        endpoint = html_body_parser.parse("")
        assert endpoint is None
