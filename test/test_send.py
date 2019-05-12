import unittest

import pytest

import webmentiontools
from webmentiontools.send import WebmentionSend

MOCK_SOURCE = 'http://example.com/'
MOCK_TARGET = 'http://foo.bar/'

WEBMENTION_ROCKS_TESTS = [{
    "test": "https://webmention.rocks/test/1",
    "endpoint": "https://webmention.rocks/test/1/webmention?head=true"
}, {
    "test": "https://webmention.rocks/test/2",
    "endpoint": "https://webmention.rocks/test/2/webmention?head=true"
}, {
    "test": "https://webmention.rocks/test/3",
    "endpoint": "https://webmention.rocks/test/3/webmention"
}, {
    "test": "https://webmention.rocks/test/4",
    "endpoint": "https://webmention.rocks/test/4/webmention"
}, {
    "test": "https://webmention.rocks/test/5",
    "endpoint": "https://webmention.rocks/test/5/webmention"
}, {
    "test": "https://webmention.rocks/test/6",
    "endpoint": "https://webmention.rocks/test/6/webmention"
}, {
    "test": "https://webmention.rocks/test/7",
    "endpoint": "https://webmention.rocks/test/7/webmention?head=true"
}, {
    "test": "https://webmention.rocks/test/8",
    "endpoint": "https://webmention.rocks/test/8/webmention?head=true"
}, {
    "test": "https://webmention.rocks/test/9",
    "endpoint": "https://webmention.rocks/test/9/webmention"
}, {
    "test": "https://webmention.rocks/test/10",
    "endpoint": "https://webmention.rocks/test/10/webmention?head=true"
}, {
    "test": "https://webmention.rocks/test/11",
    "endpoint": "https://webmention.rocks/test/11/webmention"
}, {
    "test": "https://webmention.rocks/test/12",
    "endpoint": "https://webmention.rocks/test/12/webmention"
}, {
    "test": "https://webmention.rocks/test/13",
    "endpoint": "https://webmention.rocks/test/13/webmention"
}, {
    "test": "https://webmention.rocks/test/14",
    "endpoint": "https://webmention.rocks/test/14/webmention"
}, {
    "test": "https://webmention.rocks/test/15",
    "endpoint": "https://webmention.rocks/test/15"
}, {
    "test": "https://webmention.rocks/test/16",
    "endpoint": "https://webmention.rocks/test/16/webmention"
}, {
    "test": "https://webmention.rocks/test/17",
    "endpoint": "https://webmention.rocks/test/17/webmention"
}, {
    "test": "https://webmention.rocks/test/18",
    "endpoint": "https://webmention.rocks/test/18/webmention?head=true"
}, {
    "test": "https://webmention.rocks/test/19",
    "endpoint": "https://webmention.rocks/test/19/webmention?head=true"
}, {
    "test": "https://webmention.rocks/test/20",
    "endpoint": "https://webmention.rocks/test/20/webmention"
}, {
    "test": "https://webmention.rocks/test/21",
    "endpoint": "https://webmention.rocks/test/21/webmention?query=yes"
}, {
    "test": "https://webmention.rocks/test/22",
    "endpoint": "https://webmention.rocks/test/22/webmention"
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
            if not endpoint:
                continue

            assert endpoint == webmention_rock["endpoint"]

    @pytest.mark.webtest
    def test_get_final_target_url(self):
        MOCK_TARGET = "https://webmention.rocks/test/23/page"
        webmention = WebmentionSend(
            MOCK_SOURCE,
            MOCK_TARGET
        )

        endpoint = webmention.head_url()

        # This assertion is meh, because the URLs contain a changing element
        # Thus I can't just compare against a fixed string
        assert "webmention-endpoint" in endpoint

    @pytest.mark.webtest
    def test_parse_links_in_html(self):
        for webmention_rock in WEBMENTION_ROCKS_TESTS:
            webmention = WebmentionSend(
                MOCK_SOURCE,
                webmention_rock["test"]
            )
            endpoint = webmention.head_url()
            if endpoint:
                continue

            html = webmention.get_url()
            links = webmention.find_webmention_links(html)
            endpoint = links[0]
            assert endpoint == webmention_rock["endpoint"]

    def test_set_user_agent(self):
        webmention = WebmentionSend(
            MOCK_SOURCE,
            MOCK_TARGET
        )
        assert "Webmention" in webmention.user_agent
        assert webmentiontools.__version__ in webmention.user_agent
        assert "requests" in webmention.user_agent
