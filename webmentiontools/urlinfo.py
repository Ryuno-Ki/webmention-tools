#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup

class UrlInfo():

    def __init__(self, url):
        self.url = url
        self.error = False
        self.fetchHTML()

    def fetchHTML(self):
        self.soup = None
        r = requests.get(self.url)
        if r.status_code != 200:
            self.error = True
            return
        self.soup = BeautifulSoup(r.text)

    def inReplyTo(self):
        # Identify first class="u-in-reply-to" or rel="in-reply-to" link
        ir2 = self.soup.find('a', attrs={'class':'u-in-reply-to'})
        if not ir2:
            ir2 = self.soup.find('a', attrs={'rel':'in-reply-to'})
            if not ir2:
                return None
        ir2_link = ir2['href']
        return ir2_link

    def pubDate(self):
        # Get the time of the reply, if possible
        ir2_time = self.soup.find(True, attrs={'class':'dt-published'})
        if ir2_time  and ir2_time.has_attr('datetime') :
            return ir2_time['datetime']
        
    def title(self):
        # Get the title
        title = self.soup.find('title').string
        return title

    def image(self):
        author = self.soup.find(True, attrs={'class':'p-author'})
        if author:
            image = author.find('img')
            if image:
                image_src = image['src']
                return image_src
        hcard = self.soup.find(True, attrs={'class':'h-card'})
        if hcard:
            image = hcard.find('img', attrs={'class':'u-photo'})
            if image:
                return image['src']


if __name__ == '__main__':
   url = 'enter a url to test here'
   a = UrlInfo(url)
   if not a.error:
       print
       print a.inReplyTo()
       print a.pubDate()
       print a.title()
       print a.image()
