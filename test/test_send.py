import unittest

import pytest

from webmentiontools.send import WebmentionSend

MOCK_SOURCE = 'http://example.com/'


class WebmentionSendTestCase(unittest.TestCase):
    @pytest.mark.with_domain
    @pytest.mark.integration
    @pytest.mark.skip(reason="Currently receiving a 400 back")
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
    @pytest.mark.integration
    @pytest.mark.skip(reason="Currently receiving a 400 back")
    def test_delete_webmention(self):
        webmention = WebmentionSend(
            MOCK_SOURCE,
            "https://webmention.rocks/delete/1"
        )

        ok = webmention.delete_webmention()
        assert ok is True
