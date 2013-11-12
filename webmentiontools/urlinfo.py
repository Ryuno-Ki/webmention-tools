#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
from urlparse import urljoin

class UrlInfo():

    def __init__(self, url):
        self.url = url
        self.error = False
        self.fetchHTML()

    def fetchHTML(self):
        self.soup = None
        self.data = dict()
        self.data['links_to'] = []
        r = requests.get(self.url)
        if r.status_code != 200:
            self.error = True
            return
        self.soup = BeautifulSoup(r.text)

    def inReplyTo(self):
        if self.data.has_key('in_reply_to'):
            return self.data['in_reply_to']
        # Identify first class="u-in-reply-to" or rel="in-reply-to" link
        ir2 = self.soup.find('a', attrs={'class':'u-in-reply-to'})
        if not ir2:
            ir2 = self.soup.find('a', attrs={'rel':'in-reply-to'})
            if not ir2:
                return None
        ir2_link = ir2['href']
        self.data['in_reply_to'] = ir2_link
        return ir2_link

    def pubDate(self):
        # Get the time of the reply, if possible
        if self.data.has_key('pubDate'):
            return self.data['pubDate']

        ir2_time = self.soup.find(True, attrs={'class':'dt-published'})
        if ir2_time  and ir2_time.has_attr('datetime') :
            self.data['pubDate'] = ir2_time['datetime']
            return ir2_time['datetime']
        
    def title(self):
        if self.data.has_key('title'):
            return self.data['title']
        # Get the title
        title = self.soup.find('title').string
        self.data['title'] = title
        return title

    def image(self):
        if self.data.has_key('image'):
            return self.data['image']

        #Try using p-author
        author = self.soup.find(True, attrs={'class':'p-author'})
        if author:
            image = author.find('img')
            if image:
                image_src = image['src']
                self.data['image'] = urljoin(self.url, image_src)
                return self.data['image']

        # Try using h-card
        hcard = self.soup.find(True, attrs={'class':'h-card'})
        if hcard:
            image = hcard.find('img', attrs={'class':'u-photo'})
            if image:
                self.data['image'] = urljoin(self.url, image['src'])
                return self.data['image']

        # Last resort: try using rel="apple-touch-icon-precomposed"
        apple_icon = self.soup.find('link', attrs={'rel':'apple-touch-icon-precomposed'})
        if apple_icon:
            image = apple_icon['href']
            if image:
                self.data['image'] = urljoin(self.url, image)
                return self.data['image']

    def snippetWithLink(self, url):
        """ This method will try to return the first
        <p> or <div> that contains an <a> tag linking to
        the given URL.
        """
        link = self.soup.find("a", attrs={'href': url})
        if link:
            for p in link.parents:
                if p.name in ('p','div'):
                    return ' '.join(p.text.split()[0:30])
        return None


    def linksTo(self, url):
        # Check if page links to a specific URL.
        # please note that the test is done on the *exact* URL. If
        # you want to ignore ?parameters, please remove them in advance
        if url in self.data['links_to']:
            return True
        r = self.soup.find("a", attrs={'href': url})
        if r:
            self.data['links_to'].append(url)
            return True
        else:
            return False

if __name__ == '__main__':
   pass
