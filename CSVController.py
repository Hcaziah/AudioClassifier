import csv
import os
import pandas as pd
from datetime import datetime
from IOController import FileController


class CSVController:
    def __init__(self):
        self.folder = None
        self.csv_file = None
        self.folder_files = None
        self._csv_header = [
            "file_name",
            "classification",
            "file_length(sec)",
            "date",
        ]

    def open_folder_w_csv(self, folder_path) -> None:
        self.folder = folder_path
        self.folder_files = self._get_folder_files()
        self.csv_file = self._get_or_create_csv()

    def _get_folder_files(self):
        folder_files = [
            FileController(self.folder + "/" + f) for f in os.listdir(self.folder)
        ]
        return sorted(folder_files, key=lambda x: x.file_name)

    def _get_or_create_csv(self):
        """_summary_

        Raises:
            FileNotFoundError: _description_

        Returns:
            _type_: _description_
        """
        try:
            csv_file_from_list = [
                f for f in self.folder_files if f.file_extension == "csv"
            ][0]

            if csv_file_from_list:
                csv_file = FileController(
                    f"{self.folder}/{csv_file_from_list}")
                print(f"{csv_file.file_name_full} is present in folder.")
            else:
                raise FileNotFoundError()

        except (IndexError, FileNotFoundError):
            new_csv_name = f"{os.path.basename(self.folder)}.csv"
            self.create_csv(new_csv_name)
            csv_file = FileController(f"{self.folder}/{new_csv_name}")

            print(f"No csv file present\nWriting new file as {new_csv_name}")

        return csv_file

    def create_csv(self, file_name) -> None:
        with open(self.folder + "/" + file_name, "w", encoding="utf8") as csvfile:
            self.csv_file = FileController(f"{self.folder}/{file_name}")
            writer = csv.writer(csvfile)
            writer.writerow(self._csv_header)

            for f in self.folder_files:
                writer.writerow(
                    [
                        f.file_name_full,
                        None,
                        format(f.audio_length, ".3f"),
                        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    ]
                )

    def update_csv(self, index, classification):
        if self.csv_file:
            data = pd.read_csv(self.csv_file.file_path)
            data.at[index, "classification"] = classification
            data.at[index, "date"] = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S")
            data.to_csv(self.csv_file.file_path, index=False)

            print(f"updated row {index} with {classification}")

        else:
            raise FileNotFoundError()
            