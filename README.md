# Webpage display and loading time analyzer
-->Scripts:
firefox-driver.py: the main script for capture the screenshots of webpages and measure the loading time of the page. The captured images are saved to "screenshots" folder, the loading times are written to local file
ImageAnalyzer.py: analyzing the difference between two images(PNG), giving a numerical result

-->Configuration:
config: the config parameter for the firfox-driver.py, it contains the fireforx profile, logging file name and path

-->Archive: 
contains url list from Alexa top list

## Required packages
1. pip
  install pip at https://bootstrap.pypa.io/get-pip.py
2. selenium
  install selenium : pip install selenium
   
## Brief steps

1. crawl Alexa top sites and save it to archive folder

2. configure your firefox browser to have at least two profiles, one with proxy another without it. Correlate the id of the
profile in the "config" file

3. specify the log file name and path to be saved

4. run the firefox-driver script: python firefox-dirver.py config

5. collect the screenshots images for differences processing, using the ImageAnalyzer module
