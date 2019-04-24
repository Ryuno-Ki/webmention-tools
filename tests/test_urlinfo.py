import unittest

import requests_mock
from webmentiontools.urlinfo import UrlInfo

mock_url = 'http://example.com'


class UrlInfoTestCase(unittest.TestCase):

    @requests_mock.mock()
    def test_init(self, m):
        m.get(mock_url, json={'error': 'not found'}, status_code=404)
        url_info = UrlInfo(mock_url)
        self.assertEqual(url_info.url, mock_url)
        self.assertEqual(url_info.soup, None)
        self.assertEqual(url_info.data, {'links_to': []})
        self.assertTrue(url_info.error)

    @requests_mock.mock()
    def test_fetchHTML(self, m):
        m.get(mock_url, json={'error': 'not found'}, status_code=404)
        url_info = UrlInfo(mock_url)
        self.assertEqual(url_info.soup, None)
        self.assertEqual(url_info.data, {'links_to': []})
        self.assertTrue(url_info.error)

    def test_inReplyTo(self):
        mock_reply_to = 'http://in.reply/to'
        url_info = UrlInfo(mock_url)
        url_info.data['in_reply_to'] = mock_reply_to
        in_reply_to = url_info.inReplyTo()
        self.assertEqual(in_reply_to, mock_reply_to)

    def test_pubDate(self):
        mock_pubDate = 'now'
        url_info = UrlInfo(mock_url)
        url_info.data['pubDate'] = mock_pubDate
        pubDate = url_info.pubDate()
        self.assertEqual(pubDate, mock_pubDate)

    def test_title(self):
        mock_title = 'Hello, World!'
        url_info = UrlInfo(mock_url)
        url_info.data['title'] = mock_title
        title = url_info.title()
        self.assertEqual(title, mock_title)

    def test_image(self):
        mock_image = 'Look'
        url_info = UrlInfo(mock_url)
        url_info.data['image'] = mock_image
        image = url_info.image()
        self.assertEqual(image, mock_image)

    def test_snippetWithLink(self):
        mock_url = 'https://http.cat/200'
        url_info = UrlInfo(mock_url)
        mock_snippet = url_info.snippetWithLink(mock_url)
        self.assertEqual(mock_snippet, None)

    def test_linksTo(self):
        mock_links_to = 'https://http.cat/404'
        url_info = UrlInfo(mock_url)
        links_to = url_info.linksTo(mock_links_to)
        self.assertEqual(links_to, False)


if __name__ == '__main__':
    unittest.main()
