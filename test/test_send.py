import unittest

import requests_mock
from webmentiontools.send import WebmentionSend

mock_source = 'http://example.com'
mock_target = 'http://foo.bar'
mock_endpoint = 'http://webmention/endpoint'


class WebmentionSendTestCase(unittest.TestCase):
    def test_init(self):
        webmention_send = WebmentionSend(mock_source, mock_target)
        self.assertEqual(webmention_send.source_url, mock_source)
        self.assertEqual(webmention_send.target_url, mock_target)
        self.assertEqual(webmention_send.receiver_endpoint, None)

    def test_init_with_endpoint(self):
        webmention_send = WebmentionSend(
            mock_source,
            mock_target,
            mock_endpoint
        )
        self.assertEqual(webmention_send.source_url, mock_source)
        self.assertEqual(webmention_send.target_url, mock_target)
        self.assertEqual(webmention_send.receiver_endpoint, mock_endpoint)

    # The following test need more love, i.e. aren't covering everything
    @requests_mock.mock()
    def test_send(self, m):
        mock_kwargs = {}
        m.get(mock_target, json={'error': 'not found'},
                      status_code=404)

        webmention_send = WebmentionSend(
            mock_source,
            mock_target
        )
        result = webmention_send.send(**mock_kwargs)
        self.assertFalse(result)

    # The following test need more love, i.e. aren't covering everything
    @requests_mock.mock()
    def test_send_with_endpoint(self, m):
        mock_kwargs = {'headers': {'X-Clacks-Overhead': 'GNU Terry Pratchett'}}
        m.post(mock_endpoint, json={'error': 'not found'}, status_code=404)

        webmention_send = WebmentionSend(
            mock_source,
            mock_target,
            mock_endpoint
        )
        result = webmention_send.send(**mock_kwargs)
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
