#!/usr/bin/python
import os
import sys

def getlines(msg):
  print msg
  ret = '';
  while 1:
    line = raw_input()
    if line == '':
      break
    ret = ret + line + '\n'
  return ret

def callcmd(cmd):
  print 'run cmd:' + cmd
  os.system(cmd)

print "Please input subject name:"
sname = raw_input()
cmd = 'mkdir %s' % (sname)
callcmd(cmd)

os.chdir(sname)

while 1:
  print 'Please input class name(0 to exit):'
  cname = raw_input()
  if cname == '0':
    break
  curl = getlines('curl file(end with blank line:\\n):')

  cmd = 'mkdir ' + cname
  callcmd(cmd)
  #os.system(cmd)

  #cmd = 'curl -o' + cname + '/list.m3u8 ' + curl[4:]
  fo = open(cname + '/list.m3u8', "w")
  fo.write(curl)
  fo.close()
  #os.system(cmd)



cmd = 'cp ../%s.txt .' % (sname)
callcmd(cmd)
