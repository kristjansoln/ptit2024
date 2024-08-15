import speech_recognition as sr
# r = sr.Recognizer()
# with sr.Microphone() as source:
#      r.adjust_for_ambient_noise(source)  # here
#      print("Say something!")
#      audio = r.listen(source)

for index, name in enumerate(sr.Microphone.list_microphone_names()):
    print(
        'Microphone with name "{1}" found for `Microphone(device_index={0})`'.format(
            index, name
        )
    )
