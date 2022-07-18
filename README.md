# Python reverse shell ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

This project is an example of an reverse shell using python. There are provided 2 server files a single connection server and a multi connection server.

## Usage
### Single connection server: 

1. Run the server on the "attacker" machine

```
$ ./server.py
```
2. Run the client on the "victim" machine
```
$ ./reverse_shell.py
```
Send "close" to close the connection

### Multi-connection server: 

1. Run the server on the "attacker" machine

```
$ ./threader_server.py
```
2. Run the client on the "victim(s)" machine

```
$ ./reverse_shell.py
```
Control center commands:
```
targets: List all connections to the server
session [n]:    Connect to a session. Once connected the you can esecute commands on the client machine. 
                Send "q" to return to control center without stopping the connection. Send "close" to disconnect the client.
sendall [command]: Send a command to all the connected clients
screenshot: Take a screenshot on the client machine
start [command]: Start a program without blocking the shell
get [url]: Download a file from the internet
exit: Turn off the server and close all connections
help: Show this message

```
