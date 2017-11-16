#!/usr/bin/env python

import collections
import time
import json
import subprocess
import re
import sys

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

def runSiege(n, r, server):
  CONCURRENT = n
  REPS = r
  SERVER = server
  DELAY = 1

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

def toJson(d, name):
  with open(name, 'a') as out:
    json.dump(d, out)
    out.write('\n')

def repeat(concurrent, it, url):
  for i in range(1, it+1):
    d = runSiege(10**concurrent, 10, url)
    d['concurrent'] = 10**concurrent
    d['iteration'] = i
    toJson(d, 'evaluation.json')

def main(n, r, url):
  for i in range(0,n):
    repeat(i,r, url)

main(int(sys.argv[1]), int(sys.argv[2]), sys.argv[3])
