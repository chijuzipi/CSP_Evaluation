import sys, time, os, threading
from PIL import Image 
import pyscreenshot as ImageGrab
from urlparse import urlparse
import shutil
import socket
import os.path

def compare(img1, img2):
  
  domain = img1[14:]
  divid = domain.split('_')
  domain = '.'.join(divid[:len(divid)-1])
  print domain
  picture_similar = calc_similar_by_path(img1, img2)
  print "page similarity: " + str(picture_similar)
  print 
  return picture_similar


def make_regalur_image(img, size = (256, 256)):
    return img.resize(size).convert('RGB')

def split_image(img, part_size = (64, 64)):
	w, h = img.size
	pw, ph = part_size
	assert w % pw == h % ph == 0
	return [img.crop((i, j, i+pw, j+ph)).copy() \
                for i in xrange(0, w, pw) \
                for j in xrange(0, h, ph)]

def hist_similar(lh, rh):
	assert len(lh) == len(rh)
	return sum(1 - (0 if l == r else float(abs(l - r))/max(l, r)) for l, r in zip(lh, rh))/len(lh)

def calc_similar(li, ri):
	return sum(hist_similar(l.histogram(), r.histogram()) for l, r in zip(split_image(li), split_image(ri))) / 16.0

def calc_similar_by_path(lf, rf):
	li, ri = make_regalur_image(Image.open(lf)), make_regalur_image(Image.open(rf))
	return calc_similar(li, ri)

def readHostList(filePath):
  f = open(filePath)
  data = []
  for line in f:
    line = line.strip()
    data.append(line)
  return data

def getDomain(url):
  divid  = urlparse(url).hostname.split('.')
  domain = '_'.join(divid[1:])
  return domain

def getFileList():
  out1 = []
  out2 = []

  urlList = readHostList('archive/AlexaTopListGlobal.txt')
  
  for url in urlList:
    domain = getDomain(url)
    fileName1 = domain + '_1.png'
    fileName2 = domain + '_2.png'
    out1.append(fileName1)
    out2.append(fileName2)
  return out1, out2


def main():
 # for i in range(1, 500):
  fileList1, fileList2 = getFileList()
  for i in range(len(fileList1)):
    file1 = fileList1[i]
    file1 = './screenshots/' + file1
    file2 = fileList2[i]
    file2 = './screenshots/' + file2
    if os.path.isfile(file1) and os.path.isfile(file2):
      simi = compare(file1, file2)

if __name__ == "__main__":
	main()
	
