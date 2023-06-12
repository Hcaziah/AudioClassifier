import csv
import os
from datetime import datetime
from file_controller import FileController


class CSVController:
    """
    CSVController is a class that handles the creation and updating of csv files
    for the purpose of storing the classification of audio files.
    """

    def __init__(self, folder_path=None) -> None:
        self.folder = folder_path
        self.csv_file = None
        self.folder_files = None
        self._csv_header = [
            "file_name",
            "classification",
            "file_length(sec)",
            "date",
        ]

    def open_folder(self, folder_path) -> None:
        """
        open_folder is a method that opens a folder and creates a csv file

        Parameters
        ----------
        folder_path : str
            The path to the folder to be opened.
        """
        self.folder = folder_path
        self._get_folder_files()
        self._get_or_create_csv()

    def _get_folder_files(self) -> None:
        folder_files = [
            FileController(self.folder + "/" + f) for f in os.listdir(self.folder)
        ]
        self.folder_files = sorted(folder_files, key=lambda x: x.file_name)

    def _get_or_create_csv(self) -> None:
        try:
            csv_file_from_list = [
                f for f in self.folder_files if f.file_extension == "csv"
            ][0]

            if csv_file_from_list:
                self.csv_file = FileController(
                    f"{self.folder}/{csv_file_from_list}.csv"
                )
                print(f"{self.csv_file.file_name_full} is present in folder.")
            else:
                raise FileNotFoundError()

        except (IndexError, FileNotFoundError):
            new_csv_name = f"{os.path.basename(self.folder)}.csv"
            self.create_csv(new_csv_name)
            self.csv_file = FileController(f"{self.folder}/{new_csv_name}")

            print(f"No csv file present\nWriting new file as {new_csv_name}")

    def create_csv(self, file_name) -> None:
        """
        create_csv creates a csv file with the name file_name in the folder

        Parameters
        ----------
        file_name : str
            The name of the csv file to be created.
        """
        with open(
            self.folder + "/" + file_name, "w", encoding="utf8", newline=""
        ) as csvfile:
            self.csv_file = FileController(f"{self.folder}/{file_name}")
            writer = csv.writer(csvfile)
            writer.writerow(self._csv_header)

            for file in self.folder_files:
                writer.writerow(
                    (
                        file.file_name_full,
                        None,
                        format(file.audio_length, ".3f"),
                        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    )
                )

    def set_classification(self, index, classification) -> None:
        """
        update_csv is a method that updates the classification of a file in the csv file

        Parameters
        ----------
        index : int
            The index of the file in the csv file.
        classification : str
            The classification of the file.

        Raises
        ------
        FileNotFoundError
            If the csv file is not found.
        """

        if index == 0:
            return

        with open(self.csv_file.file_path, "r", encoding="utf8", newline="") as csvfile:
            reader = csv.reader(csvfile)
            data = list(reader)

        data[index][1] = classification

        with open(self.csv_file.file_path, "w", encoding="utf8", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(data)

    def get_classification(self, index) -> str:
        """
        get_csv_data is a method that returns the classification of a file in the csv file

        Parameters
        ----------
        index : int
            The index of the file in the csv file.

        Returns
        -------
        str
            The classification of the file.
        """
        with open(self.csv_file.file_path, "r", encoding="utf8", newline="") as csvfile:
            reader = csv.reader(csvfile)
            data = list(reader)

        return data[index][1]
