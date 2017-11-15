#!/usr/bin/env python

import matplotlib.pyplot as plt
import collections
import time
import json
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

xx = []
yy = collections.defaultdict(list)
def plotDynDict(d, labels, x):
  #y = d[label]
  y = []
  for l in labels:
    yy[l].append(d[l])

  xx.append(x)

  for k,v in yy.items():
    print k, ':', v
    plt.plot(xx,v, '-o')
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


def main(k):
  plt.ion()
  for i in range(1,10000):
    n = i*10
    print '>>> client:', 1, ' ', n
    plotDynDict(runSiege(n, 10, '192.168.99.100:30001'),\
    ['Response time', "Failed transactions", "Transaction rate",\
    "Throughput", "Longest transaction", "Shortest transaction"], n)
    #time.sleep(10)

  #print ">>> >>> END"
  
    result = {}
    result['iteration'] = k
    result['client'] = n
    result['values'] = yy
    with open('evaluation.json', 'a') as out:
     json.dump(result, out)
     out.write('\n')

for i in range(0,30):
  del xx[:]
  for k,v in yy.items():
    del v[:]
  main(i)
