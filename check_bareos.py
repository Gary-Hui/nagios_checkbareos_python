#! /usr/bin/python

import os
import sys
import commands
import re

okStatus = ['C', 'R', 'T']
warningStatus = ['F', 'S', 'm', 'M', 's', 'j', 'c', 'd', 't', 'p', 'i', 'a', 'W']

bareosDir = "/etc/bareos"
bacularDir = "/etc/bacula"
workingDir = ""
job=sys.argv[1]

if os.path.exists(bareosDir):
  workingDir = bareosDir
elif os.path.exists(baculaDir):
  workingDir = baculaDir
else:
  print("UNKNOW: CAN'T DETECT BAREOS/BACULA")
  sys.exit(3)

check_command="echo \"list job=" + job + "\"" +  " | /usr/sbin/bconsole -c /etc/bareos/bconsole.conf"
status, cmd = commands.getstatusoutput(check_command)
jobs=cmd.split("\n")

jobRow=""

for line in jobs:
  if re.findall('^\|\s*[0-9]+.*', line):
    jobRow = line.split('|')

if len(jobRow) == 0:
  print "UNKNWON: JOB NOT FOUND!"
  sys.exit(3)

jobStatus = jobRow[9]

jobStatus=jobStatus.replace(' ', '')

if jobStatus in okStatus:
  print('OK:' + "".join(jobRow))
  sys.exit(0)
  
elif jobStatus in warningStatus:
  print ('WARNING' + "".join(jobRow))
  sys.exit(1)
else:
  print ('CRITICAL' + "".join(jobRow))
  sys.exit(2)
