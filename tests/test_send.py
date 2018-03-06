import unittest

import responses
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
    @responses.activate
    def test_send(self):
        mock_kwargs = {}
        responses.add(responses.GET, mock_target, json={'error': 'not found'},
                      status=404)

        webmention_send = WebmentionSend(
            mock_source,
            mock_target
        )
        result = webmention_send.send(**mock_kwargs)
        self.assertFalse(result)

    # The following test need more love, i.e. aren't covering everything
    @responses.activate
    def test_send_with_endpoint(self):
        mock_kwargs = {'headers': {'X-Clacks-Overhead': 'GNU Terry Pratchett'}}
        responses.add(responses.POST,
                      mock_endpoint,
                      json={'error': 'not found'},
                      status=404)

        webmention_send = WebmentionSend(
            mock_source,
            mock_target,
            mock_endpoint
        )
        result = webmention_send.send(**mock_kwargs)
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
