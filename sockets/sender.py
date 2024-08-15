import socket
import getch

UDP_IP = "127.0.0.1"
UDP_PORT = 15005

print("Listening to keyboard and sending the characters over the network...")
print("UDP target IP: %s" % UDP_IP)
print("UDP target port: %s" % UDP_PORT)

sock = socket.socket(
    socket.AF_INET,  # Internet
    socket.SOCK_DGRAM,
)  # UDP

while True:
    MESSAGE = input("yo whaddyup")
    sock.sendto(bytes(MESSAGE, "utf8"), (UDP_IP, UDP_PORT))
