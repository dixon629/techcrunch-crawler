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
    rules = [Rule(SgmlLinkExtractor(allow=(link_crawl)), callback='parse_item', follow=True)]
    def parse_item(self, response):

        sel = Selector(response)
        soup = BeautifulSoup(response.body)
        tag = soup.findAll('h2',{'class':"post-title"})
        timestamp = soup.findAll('time', {'class':'timestamp'})
        data = {}
        final = []
        for elem in range(len(tag)):
            a = tag[elem].find('a')
            data["model"] = "contacts.news"
            data["pk"] = elem+1
            data['fields'] = {}
            data['fields']['link'] = a['href']
            data['fields']['text'] = a.text
            data['fields']['timestamp'] = timestamp[elem].text
            final.append(data)
        print json.dumps(final, indent=2)
