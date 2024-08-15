import os
from openai import OpenAI

file_name = "_temp.mp3"
language = "sl"  # IETF language tag
# language = 'en'

client = OpenAI()


def speak(text):
    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input="Today is a wonderful day to build something people love!",
    )
    response.stream_to_file(file_name)
    os.system(f"ffplay {file_name} -nodisp -autoexit")
    # os.remove(file_name)


text = "To je testni posnetek. Jaz sem Roomba in se rad peljem naprej in nazaj. Kako si? Ide gas."
speak(text)


# speech_file_path = Path(__file__).parent / "speech.mp3"
