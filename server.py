#!/usr/bin/python

import socket, json, struct
import readline

def send_frame(target,data):
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
        frame += target.recv(min(1024,frame_len-len(frame)))
    return json.loads(frame.decode("utf-8"))


def reliable_send(target,data):
    json_data = json.dumps(data).encode("utf-8")
    send_frame(target,json_data)

   

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("0.0.0.0",11221))
s.listen(1)
print("Listening for connections")

target, ip = s.accept()
print("Connection established from %s" %str(ip))
while True:
    cmd = input(f"{ip}~$ ")
    reliable_send(target,cmd)
    if(cmd =="q"):
        break
    message = receive_frame(target)
    if message:
        print(f"{ip}~$ {message}",flush=True)     
s.close()



