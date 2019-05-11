import unittest

import pytest
from webmentiontools.send import WebmentionSend

MOCK_SOURCE = 'http://example.com/'
MOCK_TARGET = 'http://foo.bar/'

WEBMENTION_ROCKS_TESTS = [{
    "test": "https://webmention.rocks/test/1",
    "endpoint": "https://webmention.rocks/test/1/webmention?head=true"
}]


class WebmentionSendTestCase(unittest.TestCase):
    def test_init(self):
        webmention = WebmentionSend(
          MOCK_SOURCE,
          MOCK_TARGET
        )
        assert webmention.from_url == MOCK_SOURCE
        assert webmention.to_url == MOCK_TARGET

    # Conform to Webmention Protocol 3.1.1
    # https://www.w3.org/TR/webmention/#create-a-source-document-that-mentions-the-target
    def test_check_has_from_url(self):
        webmention = WebmentionSend(
          MOCK_SOURCE,
          MOCK_TARGET
        )
        assert webmention.check_has_from_url() == True

    def test_check_has_to_url(self):
        webmention = WebmentionSend(
          MOCK_SOURCE,
          MOCK_TARGET
        )
        assert webmention.check_has_to_url() == True

    # Conform to Webmention Protocol 3.1.2
    # https://www.w3.org/TR/webmention/#sender-discovers-receiver-webmention-endpoint
    @pytest.mark.webtest
    def test_head_final_target_url(self):
        for webmention_rock in WEBMENTION_ROCKS_TESTS:
            webmention = WebmentionSend(
              MOCK_SOURCE,
              webmention_rock["test"]
            )
            endpoint = webmention.head_url()
            assert endpoint == webmention_rock["endpoint"]

    def test_get_final_target_url(self):
        assert False

    def test_check_from_url_has_link_header_in_http_response(self):
        assert False

    def test_parse_links_in_html(self):
        assert False

    def test_pick_first_webmention_link_in_html(self):
        assert False

    def test_set_user_agent(self):
        assert False
