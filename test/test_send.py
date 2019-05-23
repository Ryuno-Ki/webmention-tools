import unittest

import pytest

import webmentiontools
from webmentiontools.send import WebmentionSend

from .endpoints import WEBMENTION_ROCKS_TESTS

MOCK_SOURCE = 'http://example.com/'
MOCK_TARGET = 'http://foo.bar/'


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

    @pytest.mark.with_domain
    @pytest.mark.webtest
    def test_send_notification(self):
        TARGETS = [
            "https://webmention.rocks/update/1",
            "https://webmention.rocks/update/1/part/2"
        ]

        for target in TARGETS:
            webmention = WebmentionSend(
                MOCK_SOURCE,
                target
            )

            ok = webmention.send_notification()
            assert ok is True

    @pytest.mark.with_domain
    @pytest.mark.webtest
    def test_delete_webmention(self):
        webmention = WebmentionSend(
            MOCK_SOURCE,
            "https://webmention.rocks/delete/1"
        )

        ok = webmention.delete_webmention()
        assert ok is True
