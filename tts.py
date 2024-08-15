import socket
from gtts import gTTS
from playsound import playsound
import os


def speak_text(text, lang="en"):
    # Generate speech using gTTS
    tts = gTTS(text=text, lang=lang)

    # Save the generated speech to an MP3 file
    filename = "speech.mp3"
    tts.save(filename)

    # Play the generated speech
    playsound(filename)

    # Optionally, remove the file after playing
    os.remove(filename)


def udp_listener(host, port):
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Bind the socket to the address and port
    sock.bind((host, port))

    print(f"Listening on UDP port {port}...")

    while True:
        # Receive data from the socket
        data, addr = sock.recvfrom(1024)  # Buffer size is 1024 bytes

        # Decode the received bytes into a string
        text = data.decode("utf-8")

        print(f"Received message: {text} from {addr}")

        # Speak the received text out loud
        speak_text(text)


if __name__ == "__main__":
    # Define the UDP host and port to listen on
    udp_host = "0.0.0.0"  # Listen on all network interfaces
    udp_port = 15006  # You can use any port number

    # Start the UDP listener
    udp_listener(udp_host, udp_port)

