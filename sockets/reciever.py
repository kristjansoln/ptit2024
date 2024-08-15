import socket
from sys import stdout
import time

UDP_IP = "127.0.0.1"
UDP_PORT = 15005

sock = socket.socket(
    socket.AF_INET,  # Internet
    socket.SOCK_DGRAM,
)  # UDP
sock.bind((UDP_IP, UDP_PORT))
sock.setblocking(0)

while True:
    try:
        time.sleep(0.01)
        data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes
        message = bytes.decode(data, "utf8")
        print(f"{message}, from {addr}")
        # stdout.write(message)
    except BlockingIOError:
        # Throws BlockingIOError when no data is available
        pass
