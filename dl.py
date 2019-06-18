#!/usr/bin/python
import sys
import re
import os
import urllib2
import traceback
import time

def findfile(rootdir, func, out):
  ls = os.listdir(rootdir)
  for i in range(0, len(ls)):
    path = os.path.join(rootdir, ls[i])
    if os.path.isdir(path) :
      findfile(path+"/", func, out)
    else :
      if func(path) :
        out.append(path)

def is_m3u8(name) :
  if re.search(".m3u8", name) :
    return 1
  return 0


allfile = []
findfile("./download/", is_m3u8, allfile)

def get_ts_names(m3u8file):
  ret = []
  fo = open(m3u8file, 'r')
  for line in fo.readlines():
    if re.search('.ts', line):
      ret.append(line)
  fo.close()
  return ret

def callcmd(cmd):
  print 'run cmd:' + cmd
  #os.system(cmd)


def log(msg):
  curlen = len(msg)
  global show_process_maxlen
  if curlen < show_process_maxlen:
    for i in range(0, show_process_maxlen-curlen):
      msg += ' '
  sys.stdout.write(msg + "\n")
  sys.stdout.flush()


def DownloadFile(url,savePath):
    try:
        url = url.strip()
        savePath = savePath.strip()
        
        req = urllib2.urlopen(url, timeout = 60)

        saveFile = open(savePath, 'wb')
        saveFile.write(req.read())

        saveFile.close()
        req.close()
    except:
        msg = "DOWNLOAD FAILED:" + "-->" + savePath
        log(msg)
        


global show_process_maxlen
show_process_maxlen = 0
def show_process(cur, total, msg):
  global show_process_maxlen
  show = "[" + str(cur) + "/" + str(total) + "] " + msg + "\r"
  curlen = len(show)
  if show_process_maxlen < curlen:
    show_process_maxlen = curlen
  for i in range(0, show_process_maxlen-curlen):
    show += ' '
  sys.stdout.write(show)
  sys.stdout.flush()


allts = []
for line in allfile:
  for name in get_ts_names(line):
    name = name.replace("\r", '').replace('\n', '')
    (path, _) = os.path.split(line)
    path += "/" + name
    allts.append(path)


curPos =0;
for ts in allts:
  curPos+=1
  (path, name) = os.path.split(ts)
  HOST = 'http://media.XXXXXXX.org/'
  url = HOST+name
  show_process(curPos, len(allts), url + " --> " + path)
  DownloadFile(url, ts)

