import helpers

url = "https://bigishdata.com/2017/05/11/general-tips-for-web-scraping-with-python/"
params = {} #used for ? values
headers = {'user-agent' : 'Jack Schultz, bigishdata.com, contact@bigishdata.com'}


import urllib2
import urllib
data = urllib.urlencode(params)
req = urllib2.Request(url, data, headers)
fstring = urllib2.urlopen(req).read()
helpers.write_html('urllib2', fstring)


import requests
page = requests.get(url, headers=headers)
fstring = page.text
helpers.write_html('requests', fstring.encode('UTF-8'))


import httplib
#note that the url here is split into the base and the path
conn = httplib.HTTPConnection("bigishdata.com")
conn.request("GET", "/2017/05/11/general-tips-for-web-scraping-with-python/")
response = conn.getresponse()
helpers.write_html('httplib', response.read())
conn.close()
