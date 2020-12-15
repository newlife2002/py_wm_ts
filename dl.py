#!/usr/bin/python
import sys
import re
import os
import urllib2
import traceback
import time
import argparse
from tqdm import tqdm

parser = argparse.ArgumentParser(description='Download or combine the downloaded files.')
parser.add_argument('-c', dest='check_combine', action='store_const',
                    const=1, default=0,
                    help='Combine the downloaded files.')
parser.add_argument('-t', dest='test_files', action='store_const',
                    const=1, default=0,
                    help='Test the downloaded files.')

args = parser.parse_args()

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
  #print 'run cmd:' + cmd
  os.system(cmd)


def log(msg):
  curlen = len(msg)
  global show_process_maxlen
  if curlen < show_process_maxlen:
    for i in range(0, show_process_maxlen-curlen):
      msg += ' '
  sys.stdout.write(msg + "\n")
  sys.stdout.flush()


def CheckDownloadedFile(url, savePath):
  if not os.path.exists(savePath):
    msg = "DOWNLOAD FAILED:" + "-->" + savePath
    log(msg)


def DownloadFile(url,savePath):
    try:
        url = url.strip()
        savePath = savePath.strip()
        
        req0 = urllib2.Request(url)
        req0.add_header('Referer', 'https://www.XXXXXXX.org/')
        req=urllib2.urlopen(req0,timeout=60)
        b = req.read()
        req.close()
        saveFile = open(savePath, 'wb')
        saveFile.write(b)
        saveFile.close()
    except urllib2.URLError as e:
      if hasattr(e, 'code'):
        print "Url: %s\t%s" % (url,e.code)
      elif hasattr(e, 'reason'):
        print "Url: %s\t%s" % (url,'error')
    except:
        msg = "DOWNLOAD FAILED:" + url + "-->" + savePath
        log(msg)
        
def CombineFile(fromfile, tofile):
  cmd = "cat '" + fromfile + "' >> '" + tofile + "'"
  callcmd(cmd)


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




if args.check_combine:
  print 'Begin combining .mp4 files...'
  pbar = tqdm(allts, ncols = 70)
  for ts in pbar:
    (path, name) = os.path.split(ts)
    mp4name = path + ".mp4"
    #pbar.set_description()
    CombineFile(ts, mp4name)
else:
  print "Begin downloading..."
  pbar = tqdm(allts, ncols = 70)
  for ts in pbar:
    (path, name) = os.path.split(ts)
    HOST = 'http://media.XXXXXXX.org/'
    url = HOST+name
    #pbar.set_description(url)
    if args.test_files:
      CheckDownloadedFile(url, ts)
    else:
      DownloadFile(url, ts)

