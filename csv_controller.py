import csv
import os
from datetime import datetime
from file_controller import FileController
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[logging.FileHandler("app.log"), logging.StreamHandler()],
)


class CSVController:
    """Controller class for managing CSV files and their contents.

    Attributes:
        folder (str): The path to the folder containing the CSV files.
        csv_file (FileController): The current CSV file being operated on.
        folder_files (list): List of FileController objects representing files in the folder.
        _csv_header (list): The header for the CSV file.
    """

    def __init__(self, folder_path=None) -> None:
        """Initializes the CSVController.

        Args:
            folder_path (str, optional): The path to the folder containing the CSV files.
        """
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
        """Opens a folder and initializes the CSVController with its contents.

        Args:
            folder_path (str): The path to the folder.
        """
        logging.info(f"Opening folder: {folder_path}")
        self.folder = folder_path
        self._get_folder_files()
        self._get_or_create_csv()

    def _get_folder_files(self) -> None:
        """Retrieves the list of files in the folder and sorts them.

        The files are represented as FileController objects.
        """
        folder_files = [
            FileController(self.folder + "/" + f) for f in os.listdir(self.folder)
        ]
        self.folder_files = sorted(folder_files, key=lambda x: x.file_name)
        logging.info(f"Found {len(self.folder_files)} files in folder {self.folder}")

    def _get_or_create_csv(self) -> None:
        """Retrieves an existing CSV file from the folder or creates a new one."""
        try:
            csv_file_from_list = [
                f for f in self.folder_files if f.file_extension == "csv"
            ][0]

            # This method will create a CSV file from the list of files in folder.
            if csv_file_from_list:
                self.csv_file = FileController(
                    f"{self.folder}/{csv_file_from_list}.csv"
                )
                logging.info(
                    f"{self.csv_file.file_name_full} is present in folder {self.folder}"
                )
            else:
                raise FileNotFoundError()

        except (IndexError, FileNotFoundError):
            new_csv_name = f"{os.path.basename(self.folder)}.csv"
            self._create_csv(new_csv_name)
            self.csv_file = FileController(f"{self.folder}/{new_csv_name}")

            logging.info(
                f"No csv file present\nWriting new file as {self.folder}/{new_csv_name}"
            )

    def _create_csv(self, file_name) -> None:
        """Creates a new CSV file with the given name and writes file information to it.

        Args:
            file_name (str): The name of the CSV file to create.
        """
        with open(
            self.folder + "/" + file_name, "w", encoding="utf8", newline=""
        ) as csvfile:
            self.csv_file = FileController(f"{self.folder}/{file_name}")
            writer = csv.writer(csvfile)
            writer.writerow(self._csv_header)

            # Write out the audio file names and audio length.
            for file in self.folder_files:
                logging.info(
                    f"Writing {file.file_name_full} to {self.csv_file.file_name_full}"
                )
                writer.writerow(
                    (
                        file.file_name_full,
                        None,
                        format(file.audio_length, ".3f"),
                        datetime.now().strftime("%y-%m-%d %H:%M:%S"),
                    )
                )

    def set_classification(self, index, classification) -> None:
        """Sets the classification value for a specific row in the CSV file.

        Args:
            index (int): The index of the row to update.
            classification (str): The classification value to set.
        """
        if index == 0:
            return

        logging.info(
            "Setting classification for row " + str(index) + " to " + classification
        )
        with open(self.csv_file.file_path, "r", encoding="utf8", newline="") as csvfile:
            reader = csv.reader(csvfile)
            data = list(reader)

        data[index][1] = classification

        with open(self.csv_file.file_path, "w", encoding="utf8", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(data)

    def get_classification(self, index) -> str:
        """Retrieves the classification value for a specific row in the CSV file.

        Args:
            index (int): The index of the row to retrieve.

        Returns:
            str: The classification value of the specified row.
        """
        with open(self.csv_file.file_path, "r", encoding="utf8", newline="") as csvfile:
            reader = csv.reader(csvfile)
            data = list(reader)

        return data[index][1]
