import helpers

import scrapy
from scrapy.selector import Selector

class DataSpider(scrapy.Spider):
  name = "data"
  start_urls = [
      'https://bigishdata.com/2017/05/11/general-tips-for-web-scraping-with-python/'
  ]

  desired_tags = (u'p', u'h1', u'h3', u'pre')
  text = {}

  def words_from_tags(self, tag, response):
    total = []
    div = response.xpath("//div[contains(@class, 'entry-content')]")
    for para in div.xpath(".//%s" % tag):
      combined = []
      for words in para.xpath('./descendant-or-self::*/text()'):
        combined.append(words.extract())
      total.append(' '.join(combined))
    return total

  def parse(self, response):
    selector = Selector(response=response)
    for tag in self.desired_tags:
      self.text[tag] = self.words_from_tags(tag, response)
    helpers.write_data('scrapy', self.text)
    yield self.text #how scrapy returns the json object you created
