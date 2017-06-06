import helpers

with open('page.html', 'r') as f:
  page_string = f.read()


##
## BeautifulSoup
##
from bs4 import BeautifulSoup as bs
soup = bs(page_string, "html.parser")
article = soup.find('div', {'class' : 'entry-content'})

text = {}
text['p'] = []
text['h1'] = []
text['h3'] = []
text['pre'] = []
text['imgsrc'] = []
for tag in article.contents:
  #multiple if statements here to make is easier to read
  if tag is not None and tag.name is not None:
    if tag.name == "p":
      text['p'].append(tag.text)
    elif tag.name == 'h1':
      text['h1'].append(tag.text)
    elif tag.name == 'h3':
      text['h3'].append(tag.text)
    elif tag.name == 'pre':
      text['pre'].append(tag.text)
for tag in article.findAll('img'):
  text['imgsrc'].append(tag['src'])
helpers.write_data('bs', text)

##
## LXML
##
import lxml.html
page = lxml.html.fromstring(page_string)
post = page.find_class('entry-content')[0] #0 since only one tag with that class

text = {}
text['p'] = []
text['h1'] = []
text['h3'] = []
text['pre'] = []
text['imgsrc'] = []
#test_content is needed to get all of the text within the tag, not just on the top level
for tag in post.findall('p'):
  text['p'].append(tag.text_content())
  for img in tag.findall('img'):
    text['imgsrc'].append(img.attrib['src'])
for tag in post.findall('h1'):
  text['h1'].append(tag.text_content())
for tag in post.findall('h3'):
  text['h3'].append(tag.text_content())
for tag in post.findall('pre'):
  text['pre'].append(tag.text_content())
helpers.write_data('lxml', text)



##
## HTMLParser
##
from HTMLParser import HTMLParser
import urllib

desired_tags = (u'p', u'h1', u'h3', u'pre', u'img')
class BigIshDataParser(HTMLParser):
  def __init__(self):
    HTMLParser.__init__(self)
    self.inside_entry_content = 0
    self.current_tag = None
    self.current_text = []
    self.overall_text = {}
    self.overall_text['p'] = []
    self.overall_text['h1'] = []
    self.overall_text['h3'] = []
    self.overall_text['pre'] = []
    self.overall_text['img'] = []

  def handle_starttag(self, tag, attributes):
    if self.inside_entry_content and tag in desired_tags:
      self.current_tag = tag
    if tag == 'div':
      for name, value in attributes:
        if name == 'class' and value == 'entry-content': #if this is correct div
          self.inside_entry_content += 1
          return #don't keep going through the attributes since there could be infinate, or just a ton of them
    if tag == 'img' and self.inside_entry_content: #need to deal with images here since they're only a start tag
      for attr in attributes:
        if attr[0] == 'src':
          self.overall_text['img'].append(attr[1])
          break

  def handle_endtag(self, tag):
    if tag == 'div' and self.inside_entry_content:
      self.inside_entry_content -= 1 #moving on down the divs
    if tag == self.current_tag:
      tstring = ''.join(self.current_text)
      self.overall_text[self.current_tag].append(tstring)
      self.current_text = []
      self.current_tag = None

  def handle_data(self, data):
    if self.inside_entry_content:
      self.current_text.append(data)

p = BigIshDataParser()
page_string = p.unescape(page_string.decode('UTF-8'))
p.feed(page_string)
helpers.write_data('htmlparser', p.overall_text)
p.close()


