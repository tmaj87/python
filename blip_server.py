# https://docs.python.org/2/library/socket.html
from socket import *
from time import sleep,strftime
import subprocess as sp

s = socket(AF_INET, SOCK_STREAM)
s.bind(('127.0.0.1', 8081))
s.listen(5)
s.settimeout(2)

while 1:
	try:
		c,addr = s.accept()
	except timeout:
		continue
	print strftime("%H:%M:%S %d.%m.%Y"), "new client", addr
	while 1:
		try:
			data = c.recv(256)
			if not data:
				print strftime("%H:%M:%S %d.%m.%Y"), addr, "disconnected"
				break
			if "cmdcmd" in data:
				continue
			if "cmd" in data:
				try:
					c.send("ret"+sp.check_output(data[data.find("cmd")+3:], stderr=sp.STDOUT, shell=True))
				except sp.CalledProcessError as e:
					c.send("ret"+e.output)
		except error:
			sleep(1)
	c.close()