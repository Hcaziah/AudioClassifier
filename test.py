# import os
# from classify_audio_chunks import AudioQueue

# script_directory = os.path.dirname(os.path.abspath(__file__)) + "/audio/test"
# dir_contents = []

# print(script_directory)

# for subdir, dirs, files in os.walk(script_directory):
#     dir_contents = [subdir, dirs, files]


# print(dir_contents)


# aq = AudioQueue(script_directory)

# print(aq.audio_list)


from csv_controller import CSVController

csv = CSVController()

csv.open_folder("audio/stream0")

print(csv.csv_file.file_name_full)


csv.update_csv(4, "2")
