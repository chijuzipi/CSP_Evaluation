from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import *

from urlparse import urlparse

import time
import logging
import sys
import json
import signal

failureCount = 0

#########################################
#			Selenium Utilities			#
#########################################
def openNewTab(browser):
	if sys.platform == "darwin":
		ActionChains(browser).send_keys(Keys.COMMAND, "t").perform()
		ActionChains(browser).send_keys(Keys.COMMAND, "t").perform()
	elif sys.platform == "linux2":
		ActionChains(browser).send_keys(Keys.CONTROL, "t").perform()
		ActionChains(browser).send_keys(Keys.CONTROL, "t").perform()
	else:
		logging.error("openNewTab unsupported OS: %s"%sys.platform)

def closeCurrentTab(browser):
	if sys.platform == "darwin":
		browser.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 'w')
	elif sys.platform == "linux2":
		browser.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 'w')
	else:
		logging.error("closeCurrentTab unsupported OS: %s"%sys.platform)


#########################################
#			Initialization Utilities #
#########################################
def readConfigure(file_path): 
  try:
    json_file = open(file_path)
    data = json.load(json_file)
    json_file.close()
    return data
  except Exception as e:
    logging.error("failed to parse configure file "+file_path+" "+str(e))
    return None

def readHostList(filePath):
	f = open(filePath)
	data = []
	for line in f:
		line = line.strip()
		data.append(line)
	return data


#########################################
        #		  	Main				#
#########################################
def main():

  ######### initialization logging #######
  data = readConfigure(sys.argv[1])
  if data == None:
    print("failed to read configure file") 
    return

  LOG_FILENAME = 'driver.log' 
  logging.basicConfig(filename=LOG_FILENAME, level=logging.INFO)

  ######### read initialization file #######
  logging.info("reading url list....")    
  #urlList = readHostList('./archive/AlexaTopListUSA.txt')
  urlList = readHostList('issueList.txt')
  urlList = list(set(urlList))


  logging.info("start to process urls")    
  maxPage = 100
  process(urlList, data, maxPage)

def getBrowser(profile):
    # (1) Initializing firfox web driver
  firefox_profile = webdriver.FirefoxProfile(profile)
  browser = webdriver.Firefox(firefox_profile)

  # (2) Waiting load the page time to be 30s
  browser.set_page_load_timeout(30)

  return browser

   
def process(urlList, data, maxPage):
  
  # Read the firefox profile and build browser list
  profiles = [] 
  browsers = []
  for pName in data.keys():
    profiles.append(pName) 
    browser = getBrowser(data[pName])
    browsers.append(browser)

  counter = 1
  f1 = open('loadTime.txt', 'a')
  f2 = open('issueList.txt', 'w')
  
  for url in urlList:
    if counter > maxPage:
      break
    for index in range(len(browsers)):
      browser = browsers[index] 
      print "###########################   " + str(counter) + "   #############################"
      print "using profile: " + profiles[index] + ' on '  + url
      domain = getDomain(url)
      fileName = profiles[index] + '_' + domain + '.png'
      capture(url, browser, f1, fileName, f2)
      print

    counter += 1
  '''' 
  for browser in browsers:
    browser.quit()
  '''

def capture(url, browser, f1, fileName, f2):
  startT = time.time()

  if openURL(url, browser):
    endT = time.time()
    f1.write(fileName + ' : ' + str(endT - startT) + '\n')
    f1.flush()
    takeScreenShot(browser, fileName, url, f2)
  else:
    f2.write(url + '\n')
    f2.flush()
    

def openURL(url, browser):
  print "loading url in process..."
  try:
    browser.get(url)
  except TimeoutException:
    print "####--------->Timeout, capture screenshot anyway..."
    logging.error( "####--------->Timeout, capture screenshot anyway...")
    return True
  except:
    print "####--------->load url failed, NO screenshot taking"
    logging.error( "####--------->load url failed, NO screenshot taking")
    return False
  else:
    return True 

def openTab(browser):
  print "opening tab..."
  try:
    openNewTab(browser)
  except:
    print "####---------->open new tab failed..."
    logging.error("Open new tab failed")
    openTab(browser)
  finally:
    return 
  
def closeTab(browser):
  print "closing tab..."
  try:
    closeCurrentTab(browser)
  except:
    print "####---------->closing tab failed, leave it open..."
    logging.error("closing tab failed, levae it open...")
    #closeTab(browser)
  finally:
    return 

def signal_handler(signum, frame):
  raise Exception("Timed out!")

def takeScreenShot(browser, fileName, url, f2):
  # limit the function call to be 20 sec
  signal.signal(signal.SIGALRM, signal_handler)
  signal.alarm(10)   # 20 seconds

  print "start taking screen shot..."
  try:
    browser.save_screenshot('./screenshots/' + fileName)
  except: 
    print "taking screenshot timeout, abandon...."
    f2.write(url + '\n')
    f2.flush()
    logging.error("takeing screenshot of " + url + "failed")
  finally:
    return 

def getDomain(url):
  divid  = urlparse(url).hostname.split('.')
  domain = '_'.join(divid[1:])
  return domain
  
    
if __name__ == "__main__":
	main()
	
