import pathlib
from pydub import AudioSegment


class FileController:
    """Controls operations on a file.

    Attributes:
        file_path (str): The path to the file.
        file_name (str): The name of the file without the extension.
        file_extension (str): The extension of the file.
        file_folder (pathlib.Path): The parent folder of the file.
        file_name_full (str): The full name of the file including the extension.
        audio_file (AudioSegment): The audio file if the file is an audio file, None otherwise.
        audio_length (float): The duration of the audio file in seconds if the file is an audio file, None otherwise.
    """

    def __init__(self, file_path) -> None:
        """Initializes the FileController with a file path and sets up the attributes.

        Args:
            file_path (str): The path to the file.
        """
        self.file_path = file_path
        self.file_name = pathlib.Path(self.file_path).stem
        self.file_extension = pathlib.Path(self.file_path).suffix[1:]
        self.file_folder = pathlib.Path(self.file_path).parent
        self.file_name_full = self.file_name + "." + self.file_extension

        is_audio_file = self.file_extension in ["wav", "mp3"]
        self.audio_file = (
            AudioSegment.from_file(self.file_path, self.file_extension)
            if is_audio_file
            else None
        )
        self.audio_length = self.audio_file.duration_seconds if is_audio_file else None

    def __str__(self) -> str:
        """Returns the file name as a string representation.

        Returns:
            str: The file name.
        """
        return self.file_name
