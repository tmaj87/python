from socket import *

s = socket(AF_INET, SOCK_STREAM)
s.connect(('127.0.0.1', 8081))
s.send("connected")
s.settimeout(2)

while 1:
	data = ""
	cmd = raw_input("# ")
	if cmd == "exit":
		break
	s.send("cmd"+cmd)
	try:
		while 1:
			data += s.recv(1024)
	except error:
		if not data:
			print "connection lost"
			break
		print data[3:]

s.close()