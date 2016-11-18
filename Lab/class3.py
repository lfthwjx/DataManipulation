import urllib2
response = urllib2.urlopen('https://www.liepin.com/it')
html_doc = response.read()

print response.code
print response.geturl()
print response.info().dict

from bs4 import BeautifulSoup

html_doc="<html><head><title>Wow</title></head></html>"
soup = BeautifulSoup(html_doc,"html.parser")

print soup.title.string
print soup.head.contents

import json
data = [{ 'a':'A', 'b':(2, 4), 'c':3.0 }]
print repr(data)

data_json = json.dumps(data)
print data_json

