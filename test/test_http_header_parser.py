import unittest

import pytest
import requests

import webmentiontools
from webmentiontools.http_header_parser import HttpHeaderParser

from .endpoints import WEBMENTION_ROCKS_TESTS

MOCK_URL_WITH_HEADER = WEBMENTION_ROCKS_TESTS[0]["test"]
MOCK_URL_WITHOUT_HEADER = WEBMENTION_ROCKS_TESTS[2]["test"]


class HttpHeaderParserTestCase(unittest.TestCase):
    def test_init(self):
        http_header_parser = HttpHeaderParser(MOCK_URL_WITH_HEADER)
        assert http_header_parser.url == MOCK_URL_WITH_HEADER
        assert "Webmention Tools" in http_header_parser.user_agent
        assert webmentiontools.__version__ in http_header_parser.user_agent
        assert "requests" in http_header_parser.user_agent
        assert requests.__version__ in http_header_parser.user_agent

    @pytest.mark.webtest
    def test_parse_with_header(self):
        http_header_parser = HttpHeaderParser(MOCK_URL_WITH_HEADER)
        endpoint = http_header_parser.parse()
        assert endpoint == WEBMENTION_ROCKS_TESTS[0]["endpoint"]

    @pytest.mark.webtest
    def test_parse_without_header(self):
        http_header_parser = HttpHeaderParser(MOCK_URL_WITHOUT_HEADER)
        endpoint = http_header_parser.parse()
        assert endpoint is None

    @pytest.mark.webtest
    def test_parse_without_webmention(self):
        url = "http://example.com/does/not/exist/"
        http_header_parser = HttpHeaderParser(url)
        endpoint = http_header_parser.parse()
        assert endpoint is None
