#!/usr/bin/env python3

# NOTE: this example requires PyAudio because it uses the Microphone class

import speech_recognition as sr
import Levenshtein as ls
import numpy as np
import sounddevice  # Silences ALSA warnings
import time
import socket

# VARIABLES
MAX_SPEECH_LEN = 15
# commands = ["desno", "levo", "stop", "ustavi", "naprej"]
commands = ["desno", "levo", "gor", "dol", "dol jebote"]
UDP_IP = "127.0.0.1"
UDP_PORT = 15005


# FUNCTIONS
# Runs recognition on a recorded a phrase
def run_recognition(recognizer, audio):
    # Use this to save the recording and make sure speech is clear enough
    # with open("recording.wav", "wb") as file:
    #    file.write(audio.get_wav_data())

    try:
        print("Running recognition...")
        # Recognize speech with whisper (on device)
        # speech = r.recognize_whisper(audio, language="sl", model="tiny")
        # Recognize speech with google cloud
        speech = r.recognize_google(audio, language="sl-SI")

        # Remove spaces, set to lowercase. Limit lenght of the command.
        speech = speech.replace(" ", "")
        speech = speech.lower()
        if len(speech) > MAX_SPEECH_LEN:
            speech = speech[:MAX_SPEECH_LEN]
        print("I think you said " + speech)

        # If speech is empty, we did not detect it correctly.
        if len(speech) < 0:
            raise sr.UnknownValueError

        # Compare with defined commands using Levenshtein distance
        distances = []
        for i in range(len(commands)):
            distances.append(ls.ratio(commands[i], speech))
            # print(
            #     f"Distance between {speech} and {commands[i]}: {ls.distance(commands[i], speech)}, ratio: {ls.ratio(commands[i], speech)}"
            # )

        # Find best matching command
        best_guess_index = np.argmax(distances)
        if distances[best_guess_index] > 0.3:
            comm = commands[best_guess_index]
            print(
                f"Best guess is {comm}, with distance ratio of {distances[best_guess_index]}"
            )

            # Send command over UDP
            sock.sendto(bytes(comm, "utf8"), (UDP_IP, UDP_PORT))

        else:
            print("No valid command detected.")

    except sr.UnknownValueError:
        print("Recognizer could not understand audio")
    except sr.RequestError as e:
        print(f"Could not request results from recognizer; {e}")


# MAIN

# recognizer instance
r = sr.Recognizer()

# Calibrate for ambient noise
with sr.Microphone() as source:
    r.adjust_for_ambient_noise(source, duration=1)

# Recognizer settings
# r.dynamic_energy_threshold = True
# r.dynamic_energy_adjustment_damping = 0.3
# r.dynamic_energy_adjustment_ratio = 1.5
# r.pause_threshold = 0.5
phrase_time_limit = 2.5

# Print UDP settings
print("UDP target IP: %s" % UDP_IP)
print("UDP target port: %s" % UDP_PORT)

# Define UDP socket
sock = socket.socket(
    socket.AF_INET,  # Internet
    socket.SOCK_DGRAM,
)

# Spawns a separate thread for listening
print("Listening ...")
stop_listening = r.listen_in_background(
    source=sr.Microphone(),
    callback=run_recognition,
    phrase_time_limit=phrase_time_limit,
)
try:
    # Wait forever, until Ctrl+C
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    stop_listening(wait_for_stop=False)
