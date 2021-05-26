#!/usr/bin/python
import re
import sys
import os
from html import unescape

fp = open(sys.argv[1], 'r')

line = fp.readline()

doParse = False
deleteDiv = False
videos = []

threeDashesCnt = 0
vidIndex = 0

def replaceLine(line):
    line = line.replace('http://', '//')
    line = unescape(line)
    return line

while line:
  try:
    printLine = True

    if line.strip() == "---":
      threeDashesCnt += 1

    elif line.strip() == "content:":
      doParse = True

    if doParse:
      # match = re.findall("youtu\.?be\/?\s?[a-z:\/.?]*(?:id|v)=[\"]?([\w+\-]+)[\"]?", line)
      # match = re.findall("youtu\.?be[\/|\s]*(?:id|v)?=?[\"]?([\w+\-]+)[\"]?", line)
      # match = re.findall("youtube\s?[a-z:\/.?]*(?:id|v)=[\"]?([\w+\-]+)[\"]?|youtu\.be\/(\w+)", line)
      match = re.findall("youtu\.?be\s?[a-z:\/.?]*(?:id|v|\/)=?[\"]?([\w+\-]+)[\"]?", line)
      if match and match not in videos:
        videos.append(match)

    if threeDashesCnt > 1:
      match = re.findall("<div class=\"video-shortcode\">", line)
      match2 = re.findall("<span class=[\"]?[\']?embed-youtube", line)
      if match or match2:
        print("{{% include youtube.html id=\"{}\" %}}".format(videos[vidIndex][0]))
        vidIndex += 1
        printLine = False
        deleteDiv = True

    if printLine:
      if deleteDiv and re.match("\s*</div>\s*$", line):
        deleteDiv = False
      else:
        print(line.rstrip())

    line = fp.readline()
    line = replaceLine(line)
  except Exception as e:
    print(e)
    sys.exit(1)
