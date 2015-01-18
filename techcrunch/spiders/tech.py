from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.item import Item, Field
from scrapy.spider import BaseSpider
from bs4 import BeautifulSoup
from scrapy.http import Request
import urlparse
from urlparse import urljoin
from scrapy.selector import Selector
import json

class FundsupermartSpider(CrawlSpider):

    name = 'tech_crawl'
    allowed_domains = ['techcrunch.com']
    link_crawl = 'http://techcrunch.com/popular/'
    start_urls = ['http://techcrunch.com/popular/']
    content = []
    rules = [Rule(SgmlLinkExtractor(allow=(link_crawl)), callback='parse_item', follow=True)]
    def parse_item(self, response):

        sel = Selector(response)
        soup = BeautifulSoup(response.body)
        tag = soup.findAll('h2',{'class':"post-title"})
        timestamp = soup.findAll('time', {'class':'timestamp'})
        data = {}
        final = []
        content = []
        for elem in range(len(tag)):
            a = tag[elem].find('a')
            data["model"] = "contacts.news"
            data["pk"] = elem+1
            data['fields'] = {}
            data['fields']['link'] = a['href']
            data['fields']['text'] = a.text
            data['fields']['timestamp'] = timestamp[elem]['datetime'].split(' ')[0]
            yield Request(a['href'], callback=self.parseSub)
            final.append(data)
            data = {}
        print json.dumps(final, indent=2)

    def parseSub(self, response):

        soup = BeautifulSoup(response.body)
        article = soup.find('div', {'class':"article-entry text"})
        invalid_tags = ['b', 'i', 'u', 'div', 'figure', 'a', 'html', 'body', 'p', 'h1', 'h2', 'span', 'img', 'strong', 'li', 'ul', 'figcaption', 'br', 'script', 'small']
        [s.extract() for s in article('script')]
        for tag in invalid_tags:
            for match in article.findAll(tag):
                match.replaceWithChildren()
        self.content.append(article.text)

        print json.dumps(self.content, indent=2)
