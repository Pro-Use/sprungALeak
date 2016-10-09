#!/usr/bin/python
import threading
import os
from ipList import *
from socket import *
from datetime import datetime, timedelta
import time
from numpy import recfromcsv

commands = recfromcsv('ROBOT_COMMANDS.tsv', delimiter='\t')

port = 15000

def msg(cmd, host):
	addr = (host, port)
	UDPSock = socket(AF_INET, SOCK_DGRAM)
	UDPSock.sendto(cmd, addr)
	UDPSock.close()

def sndMsg(cmdStr, IPlist, future):
	for i in range(0,len(IPlist)):
		ip = ipDict[IPlist[i]]
		cmd = cmdStr.encode('utf-8')
		timer = future - datetime.now()
		timer = (str(timer)[6:])
		print ("%s: Send %s to %s" % (future, cmd, ip)) #For debug
#		c = threading.Timer(float(timer), msg, args=[cmd, ip])
#		c.start()

startTime = datetime.now()
wait = -0.00001
for i in range(0, len(commands)):
	try:
		newWait = str(commands[i][0])[2:-1]
		min, sec = newWait.split(':')
		newWait = (int(min) * 60) + int(sec)
		cmd ="%s %s" % (str(commands[i][2])[2:-1], str(commands[i][3])[2:-1])
		while datetime.now() < startTime + timedelta(0, newWait):
			pass
		if newWait > wait:
			future = datetime.now() + timedelta(0,1)
			wait = newWait
		try:
			pis = str(commands[i][4])[2:-1].split(', ')
			sndMsg(cmd, pis, future)
		except:
			pis = str(commands[i][4])[2:-1]+','
			sndMsg(cmd, pis, future)
	except(KeyboardInterrupt, SystemExit):
		raise
	except:
		row = i + 2
		print("\trow:"+str(row))
		if len(str(commands[i][4])[2:-1]) < 2:
			print("\terr: no host")
		elif ":" not in str(commands[i][0]):
			print("\terr: %s not a valid timecode") % str(commands[i][4])[2:-1]
		else:
			print("\terr: failed, check the tsv!")
