import helpers

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

url = 'https://bigishdata.com/2017/05/11/general-tips-for-web-scraping-with-python/'

driver = webdriver.PhantomJS()
driver.get(url)
elem = driver.find_element_by_class_name('entry-content')

text = {}
desired_tags = (u'p', u'h1', u'h3', u'pre')
for tag in desired_tags:
  tags = elem.find_elements_by_tag_name(tag)
  text[tag] = []
  for data in tags:
    text[tag].append(data.text)

helpers.write_data('selenium', text)
