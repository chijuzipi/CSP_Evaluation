# Webpage display and loading time analyzer
HOW TO RUN?
"python comparator.py"

-->Scripts:
1) comparator.py: the main script for capture the screenshots of webpages and measure the loading time of the page. The captured images are saved to "screenshots" folder, the loading times are written to local file

2) ImageAnalyzer.py: analyzing the difference between two images(PNG), giving a numerical result

-->Archive: 
contains url list from Alexa top list

## Required packages
1. pip
  install pip at https://bootstrap.pypa.io/get-pip.py
2. selenium
  install selenium : pip install selenium
   
## Brief steps of how the script runs

1. crawl Alexa top 500 sites and save it to archive folder

2. load url from the url list

3. upon successful loading the webpage, screen save to local

4. collect the screenshots images for differences processing, using the ImageAnalyzer.py
