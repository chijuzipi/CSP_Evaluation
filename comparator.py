from selenium import webdriver
from selenium.common.exceptions import *
from urlparse import urlparse

from datetime import datetime
import os
import time

class Comparator:
  def __init__(self):
    #direct to the chrome file in the OS
    chromedriver = "/usr/local/Cellar/chromedriver/2.14/bin/chromedriver"
    os.environ["webdriver.chrome.driver"] = chromedriver

    # set proxy for browser 2
    '''######## HOST:PORT
    PROXY = "127.0.0.1:8080" 
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--proxy-server=%s' % PROXY)
    '''

    # for now, just use two identifical browser without proxy
    browser1 = webdriver.Chrome(chromedriver)
    browser2 = webdriver.Chrome(chromedriver)
    #browser2 = webdriver.Chrome(chrome_options=chrome_options)

    #set page loading time upper bound
    browser1.set_page_load_timeout(30)
    browser2.set_page_load_timeout(30)

    urlList = self.readHostList('archive/AlexaTopListGlobal.txt')

    loadTimeFile = self.getLoadTimeFile()
    loadTimeFile = './overhead/' + loadTimeFile
    f1 = open(loadTimeFile, 'a')
  
    counter = 1
    for url in urlList:
      print "######### " + str(counter) + " ##########" 
      domain = self.getDomain(url)
      fileName1 = domain + '_1.png'
      fileName2 = domain + '_2.png'

      t1 = self.openPage(url, browser1, fileName1)
      t2 = self.openPage(url, browser2, fileName2)

      f1.write(url + ':' + str(t1) + ':' + str(t2) + '\n')
      f1.flush()
      counter += 1
      print 
  
  def openPage(self, url, browser, fileName):
    timeDiff = 0
    startT = time.time()

    if self.openURL(url, browser):
      endT = time.time()
      timeDiff = endT - startT
      self.takeScreenShot(browser, fileName)
      return timeDiff
    else:
      return timeDiff 

  def openURL(self, url, browser):
    print "loading url: " + url +  " ......"
    try:
      browser.get(url)
    except TimeoutException:
      print "####--------->load url timeout, capture screenshot anyway..."
      return True
    except:
      print "####--------->load url failed, NO screenshot taking"
      return False
    else:
      return True 

  def takeScreenShot(self, browser, fileName):
    print "start taking screen shot..."
    try:
      browser.save_screenshot('./screenshots/' + fileName)
    except: 
      print "taking screenshot timeout, abandon...."
    finally:
      return 

  def readHostList(self, filePath):
    f = open(filePath)
    data = []
    for line in f:
      line = line.strip()
      data.append(line)
    return data

  def getDomain(self, url):
    divid  = urlparse(url).hostname.split('.')
    domain = '_'.join(divid[1:])
    return domain

  def getLoadTimeFile(self):
    curr = str(datetime.now()).split('-')
    curr = ''.join(curr)
    curr = 'LT' + curr
    curr = curr.replace(" ", "")
    curr = curr.replace(":", "")
    curr = curr.replace(".", "")
    curr = curr[:14]
    return curr

def main():
  comparator = Comparator() 

if __name__ == '__main__':
  main()
