import pathlib
from tkinter import filedialog
from pydub import AudioSegment


class FileController():
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
        # self.file_size = pathlib.Path(self.file_path).stat().st_size

        self.audio_file = AudioSegment.from_file(self.file_path, self.file_extension) if (
            self.file_extension in ["wav", "mp3"]) else None


class IOController:
    """
    A class for handling input and output operations.

    Attributes
    ----------
    current_file : str or None
        The path to the currently opened file, or None if no file is open.
    current_folder : str or None
        The path to the currently opened folder, or None if no folder is open.

    Methods
    -------
    open_audio_file()
        Opens an audio file and returns its path.
    generate_csv(csv_filename="empty_csv")
        Generates a new CSV file with the given filename.
    open_csv()
        Opens a CSV file and returns a FileController object.
    open_folder()
        Opens a folder and returns its path.
    """

    def __init__(self) -> None:
        self.current_file = None
        self.current_folder = None

    def open_audio_file(self):
        """
        Opens an audio file and returns its path.

        Returns
        -------
        str or None
            The path to the opened file, or None if the user cancels the operation.
        """
        try:
            output_file = FileController(filedialog.askopenfilename(initialdir=".", title="Select File", filetypes=(
                ("mp3 files", "*.mp3"), ("wav files", "*.wav"), ("all files", "*.*")))).audio_file
        except FileNotFoundError:
            output_file = None

        return output_file

    def generate_csv(self, csv_filename="empty_csv") -> None:
        """
        Generates a new CSV file with the given filename.

        Parameters
        ----------
        csv_filename : str, optional
            The name of the CSV file to generate (default is "empty_csv").
        """
        with open(f"{csv_filename}.csv", "w", encoding="utf8") as _:
            pass

    def open_csv(self) -> FileController:
        """
        Opens a CSV file and returns a FileController object.

        Returns
        -------
        FileController or None
            A FileController object representing the opened file, or None if the user cancels the operation.
        """
        try:
            output_file = FileController(filedialog.askopenfilename(initialdir=".", title="Select File", filetypes=(
                ("csv files", "*.csv"), ("all files", "*.*"))))
        except FileNotFoundError:
            output_file = None

        return output_file

    def open_folder(self) -> str:
        """
        Opens a folder and returns its path.

        Returns
        -------
        str or None
            The path to the opened folder, or None if the user cancels the operation.
        """
        try:
            output_folder = filedialog.askdirectory(
                initialdir='.', title="Select Output Folder")
        except FileNotFoundError:
            output_folder = None

        self.current_folder = output_folder
        return output_folder
