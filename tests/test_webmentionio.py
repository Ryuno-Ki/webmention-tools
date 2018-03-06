import unittest

from webmentiontools.webmentionio import WebmentionIO


class WebmentionIOTestCase(unittest.TestCase):

    def test_init(self):
        webmention_io = WebmentionIO()
        self.assertEqual(webmention_io.access_token, None)
        self.assertEqual(webmention_io.api_endpoint,
                         'https://webmention.io/api')

    def test_init_with_token(self):
        mock_token = 's3cr3t'
        webmention_io = WebmentionIO(mock_token)
        self.assertEqual(webmention_io.access_token, mock_token)
        self.assertEqual(webmention_io.api_endpoint,
                         'https://webmention.io/api')

    def test_api_links_req(self):
        mock_key = 'something'
        mock_value = 'different'
        webmention_io = WebmentionIO()
        content = webmention_io.api_links_req(mock_key, mock_value)
        self.assertEqual(content, False)

    def test_linksToURL(self):
        mock_url = 'http://example.com'
        webmention_io = WebmentionIO()
        links = webmention_io.linksToURL(mock_url)
        self.assertEqual(links, {'links': []})

    def test_linksToDomain(self):
        mock_domain = 'example.com'
        webmention_io = WebmentionIO()
        links = webmention_io.linksToDomain(mock_domain)
        self.assertEqual(links, False)

    def test_linksToAll(self):
        webmention_io = WebmentionIO()
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
