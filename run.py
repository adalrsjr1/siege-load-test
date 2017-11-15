#!/usr/bin/env python

import matplotlib.pyplot as plt
import time
import subprocess
import re

def outputToDict(output):
  d = dict()

  for line in output.splitlines():
    splitted = re.compile(':\s+').split(line)
    if len(splitted) == 2:
      d[splitted[0]] = float(splitted[1].split(' ')[0])

  return d

def getValues(l, label):
  values = list()
  for d in l:
     values.append(d[label])

  return values

def plotListDict(l, label):
  values = getValues(l, label)
  
  print (">>> values: ", values)

  plt.plot(values, 'bo', values, 'k')
  plt.ylabel(label)
  plt.xlabel('clients')
  plt.show()

xx = list()
yy = list()
def plotDynDict(d, label, x):
  y = d[label]
  print '>>> (',x,',',y,')'
  xx.append(x)
  yy.append(y)
  plt.plot(xx,yy, 'r-o')
  plt.pause(0.05)

def runSiege(n, r, server):
  CONCURRENT = n
  REPS = r
  SERVER = server
  DELAY = 0

  output = subprocess.Popen(['./siege.sh %s %s %s %s'%(CONCURRENT, \
  REPS, SERVER, DELAY)],\
  shell=True, stderr=subprocess.PIPE)

  output_str = ''
  while True:
    line = output.stderr.readline()
    if not line:
       break
    output_str += line
  
  return outputToDict(output_str)

l = list()

plt.ion()
for i in range(9,15):
  print '>>> client:', i+1, ' ', 2**i
  plotDynDict(runSiege(2**i, 10, '192.168.99.100:30001'),\
  'Response time', i*2+1)
  time.sleep(10)

print ">>> >>> END"

while True:
  plt.pause(0.05)

  #l.append(runSiege(i*2+1, 10, '192.168.99.100:30001'))
  #plotListDict(l, 'Response time') 
  #time.sleep(30)

#plotListDict(l, 'Response time')
