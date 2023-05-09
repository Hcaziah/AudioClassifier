import pathlib
import os
from tkinter import filedialog
from pydub import AudioSegment


class FileController:
    """
    A class for controlling audio files.

    Attributes
    ----------
    file_path : str
        The path to the audio file.
    file_name : str
        The name of the audio file.
    file_extension : str
        The extension of the audio file.
    file_folder : str
        The folder containing the audio file.
    audio_file : AudioSegment
        The audio file as an AudioSegment object.
    """

    def __init__(self, file_path) -> None:
        self.file_path = file_path
        self.file_name = pathlib.Path(self.file_path).stem
        self.file_extension = pathlib.Path(self.file_path).suffix[1:]
        self.file_folder = pathlib.Path(self.file_path).parent
        self.file_name_full = self.file_name + "." + self.file_extension
        # self.file_size = os.path.getsize(self.file_path)

        isAudioFile = self.file_extension in ["wav", "mp3"]
        self.audio_file = (
            AudioSegment.from_file(self.file_path, self.file_extension)
            if isAudioFile
            else None
        )
        self.audio_length = (
            self.audio_file.duration_seconds if isAudioFile else None
        )  # ms

    def __str__(self) -> str:
        return self.file_name
