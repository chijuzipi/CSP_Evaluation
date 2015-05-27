import urllib2, cookielib
import time, datetime
from bs4 import BeautifulSoup

class Collector:
  def __init__(self):
    cookie_support= urllib2.HTTPCookieProcessor(cookielib.CookieJar())
    opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
    urllib2.install_opener(opener)

    #urlSeed = "http://www.alexa.com/topsites/countries;" 
    urlSeed = "http://www.alexa.com/topsites/global;"
    f = open("AlexaTopListGlobal.txt", "w")
    for i in range(21):

      url = urlSeed + str(i) 

      content = urllib2.urlopen(url, timeout=120).read()
      self.parse(content, f)

  def parse(self, content, f):
    soup = BeautifulSoup(content)
    lists = soup.findAll("li", {"class" : "site-listing"})
    for item in lists:

      url = item.find("p", {"class":"desc-paragraph"})
      url = url.text
      f.write("http://www." + url)


def main():
  collector = Collector()

if __name__ == '__main__':
    main()
