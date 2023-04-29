import os
from ClassifyAudioChunks import AudioQueue

script_directory = os.path.dirname(os.path.abspath(__file__)) + "\\audio\\test"
dir_contents = []

print(script_directory)

for subdir, dirs, files in os.walk(script_directory):
    dir_contents = [subdir, dirs, files]


print(dir_contents)


aq = AudioQueue(script_directory)

print(aq.audio_list)
