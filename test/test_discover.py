import unittest

import pytest

from webmentiontools.discover import WebmentionDiscover

from .endpoints import WEBMENTION_ROCKS_TESTS

MOCK_URL = 'http://foo.bar/'


class WebmentionDiscoverTestCase(unittest.TestCase):
    def test_init(self):
        webmention = WebmentionDiscover(
            MOCK_URL
        )
        assert webmention.url == MOCK_URL

    # Conform to Webmention Protocol 3.1.1
    # https://www.w3.org/TR/webmention/#create-a-source-document-that-mentions-the-target
    def test_check_has_url(self):
        webmention = WebmentionDiscover(
            MOCK_URL
        )
        assert webmention.check_has_url() is True

    def test_check_has_url_invalid(self):
        invalid_url = "does.not.exist"
        webmention = WebmentionDiscover(
            invalid_url
        )
        assert webmention.check_has_url() is False

    # Conform to Webmention Protocol 3.1.2
    # https://www.w3.org/TR/webmention/#sender-discovers-receiver-webmention-endpoint
    @pytest.mark.integration
    def test_discover(self):
        for test in WEBMENTION_ROCKS_TESTS:
            webmention = WebmentionDiscover(test["url"])
            endpoint = webmention.discover()
            assert endpoint == test["endpoint"]

        url = "https://webmention.rocks/test/23/page"
        webmention = WebmentionDiscover(url)
        endpoint = webmention.discover()

        # This assertion is meh, because the URLs contain a changing element
        # Thus I can't just compare against a fixed string
        assert "webmention-endpoint" in endpoint

    @pytest.mark.integration
    def test_discover_no_endpoint(self):
        url = "http://example.com"
        webmention = WebmentionDiscover(url)
        endpoint = webmention.discover()
        assert endpoint is None
