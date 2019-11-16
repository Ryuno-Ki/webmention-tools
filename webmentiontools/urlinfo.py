#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scan a URL for WebMentions
"""
from urllib.parse import urljoin

from bs4 import BeautifulSoup  # type: ignore
import requests


class UrlInfo():
    """
    Gets some information about an URL.
    """
    def __init__(self, url):
        self.url = url
        self.error = False
        self.fetch_html()

    def fetch_html(self):
        """
        Parses the HTML of the site.
        """
        self.soup = None
        self.data = dict()
        self.data['links_to'] = []
        response = requests.get(self.url)
        if response.status_code != 200:
            self.error = True
            return
        # use apparent_encoding, seems to work better in the cases I tested.
        response.encoding = response.apparent_encoding
        self.soup = BeautifulSoup(response.text, 'html.parser')

    def in_reply_to(self):
        """
        Get the replies to links.
        """
        if 'in_reply_to' in self.data:
            return self.data['in_reply_to']
        # Identify first class="u-in-reply-to" or rel="in-reply-to" link
        ir2 = self.soup.find('a', attrs={'class': 'u-in-reply-to'})
        if not ir2:
            ir2 = self.soup.find('a', attrs={'rel': 'in-reply-to'})
            if not ir2:
                return None
        ir2_link = ir2['href']
        self.data['in_reply_to'] = ir2_link
        return ir2_link

    def pub_date(self):
        """
        Get the time of the reply, if possible
        """
        if 'pubDate' in self.data:
            return self.data['pubDate']

        ir2_time = self.soup.find(True, attrs={'class': 'dt-published'})
        if ir2_time and ir2_time.has_attr('datetime'):
            self.data['pubDate'] = ir2_time['datetime']
            return ir2_time['datetime']
        return None

    def title(self):
        """
        Extracts the title from the markup
        """
        if 'title' in self.data:
            return self.data['title']
        # Get the title
        title = self.soup.find('title').string
        self.data['title'] = title
        return title

    def image(self):
        """
        Gets an image for this URL.
        """
        if 'image' in self.data:
            return self.data['image']

        # Try using p-author
        author = self.soup.find(True, attrs={'class': 'p-author'})
        if author:
            image = author.find('img')
            if image:
                image_src = image['src']
                self.data['image'] = urljoin(self.url, image_src)
                return self.data['image']

        # Try using h-card
        hcard = self.soup.find(True, attrs={'class': 'h-card'})
        if hcard:
            image = hcard.find('img', attrs={'class': 'u-photo'})
            if image:
                self.data['image'] = urljoin(self.url, image['src'])
                return self.data['image']

        # Last resort: try using rel="apple-touch-icon-precomposed"
        apple_icon = self.soup.find(
            'link', attrs={'rel': 'apple-touch-icon-precomposed'}
        )
        if apple_icon:
            image = apple_icon['href']
            if image:
                self.data['image'] = urljoin(self.url, image)
                return self.data['image']
        return None

    def snippet_with_link(self, url):
        """ This method will try to return the first
        <p> or <div> that contains an <a> tag linking to
        the given URL.
        """
        link = self.soup.find("a", attrs={'href': url})
        if link:
            for parent in link.parents:
                if parent.name in ('p', 'div'):
                    return ' '.join(parent.text.split()[0:30])
        return None

    def links_to(self, url):
        """
        Check if page links to a specific URL.
        please note that the test is done on the *exact* URL. If
        you want to ignore ?parameters, please remove them in advance
        """
        if url in self.data['links_to']:
            return True
        links = self.soup.find("a", attrs={'href': url})
        if links:
            self.data['links_to'].append(url)
            return True
        return False


if __name__ == '__main__':
    pass
