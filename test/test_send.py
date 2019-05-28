import unittest

import pytest

from webmentiontools.send import WebmentionSend

MOCK_SOURCE = 'http://example.com/'
MOCK_TARGET = 'http://foo.bar/'


class WebmentionSendTestCase(unittest.TestCase):
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
