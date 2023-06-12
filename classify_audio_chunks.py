import os
import threading
from tkinter import Frame, ttk, filedialog, StringVar
import simpleaudio
from file_controller import FileController
from csv_controller import CSVController
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[logging.FileHandler("app.log"), logging.StreamHandler()],
)


class AudioQueue:
    """Represents a queue of audio files.

    Attributes:
        folder_path (str): The path to the folder containing audio files.
        current_index (int): The index of the currently playing audio file.
        audio_list (list): A list of FileController instances representing audio files.
        _playback (simpleaudio.PlayObject): The current audio playback object.
    """

    def __init__(self, folder_path=None) -> None:
        """Initializes the AudioQueue with a folder path and sets up the audio list.

        Args:
            folder_path (str, optional): The path to the folder containing audio files.
        """
        self.folder_path = folder_path
        self.current_index = 1
        self.audio_list = []
        self._playback = None

        for file in os.listdir(self.folder_path):
            if file.endswith(".csv"):
                continue
            self.audio_list.append(FileController(f"{self.folder_path}\\{file}"))

    def play_current(self) -> None:
        """Plays the currently selected audio file."""
        segment = self.audio_list[self.current_index - 1].audio_file

        self._playback = simpleaudio.play_buffer(
            segment.raw_data,
            bytes_per_sample=segment.sample_width,
            sample_rate=segment.frame_rate,
            num_channels=segment.channels,
        )

    def stop_current(self) -> None:
        """Stops the playback of the current audio file."""
        if self._playback:
            self._playback.stop()

    def next(self) -> None:
        """Moves to the next audio file in the queue and plays it."""
        logging.info("Moving to next audio file")
        self.stop_current()
        self.current_index += 1
        self.play_current()

    def prev(self) -> None:
        """Moves to the previous audio file in the queue and plays it.

        Returns:
            int: The index of the current audio file after moving to the previous one.
        """
        logging.info("Moving to previous audio file")
        self.stop_current()
        self.current_index -= 1
        self.play_current()


class ClassifyAudioChunks(Frame):
    """Represents a GUI frame for classifying audio chunks.

    Attributes:
        controller: The controller for the GUI frame.
        audio_queue (AudioQueue): The audio queue for managing audio files.
        csv_controller (CSVController): The controller for handling CSV files.
        is_shift_pressed (bool): A flag indicating whether the Shift key is currently pressed.
    """

    def __init__(self, parent, controller=None) -> None:
        """Initializes the ClassifyAudioChunks GUI frame.

        Args:
            parent: The parent widget.
            controller: The controller for the GUI frame.
        """
        Frame.__init__(self, parent)

        self.controller = controller

        self.audio_queue = None
        self.csv_controller = None

        self.is_shift_pressed = False

        # Add buttons
        button_frame = Frame(self)
        button_frame.pack(side="bottom", fill="x", padx=50, pady=10)

        self.button_next = ttk.Button(
            button_frame, text="->", command=self.next, width=5
        )
        self.allow_next = True
        self.button_prev = ttk.Button(
            button_frame, text="<-", command=self.prev, width=5
        )
        self.allow_prev = False
        self.button_replay = ttk.Button(
            button_frame, text="Select folder", command=self.open_folder, width=10
        )

        self.button_next.pack(side="right", padx=10)
        self.button_prev.pack(side="left", padx=10)
        self.button_replay.pack(side="bottom", fill="x")

        # Add text box
        self.classification_var = StringVar(value="")

        self.classification_Entry = ttk.Entry(
            self, textvariable=self.classification_var
        )
        self.classification_Entry.pack(side="bottom", fill="x", padx=10, pady=10)

        self.button_prev.config(state="disabled")
        self.button_next.config(state="disabled")

    def open_folder(self) -> None:
        """Opens a file dialog to select a folder containing audio files."""
        self.controller.bind("<Return>", self.next)

        self.controller.bind(
            "<KeyPress-Shift_L>", lambda event: setattr(self, "is_shift_pressed", True)
        )
        self.controller.bind(
            "<KeyRelease-Shift_L>",
            lambda event: setattr(self, "is_shift_pressed", False),
        )

        folder_path = filedialog.askdirectory(
            initialdir="./audio/", title="Select audio folder to classify from"
        )

        logging.info(f"Selected folder: {folder_path}")

        self.audio_queue = AudioQueue(folder_path)
        self.csv_controller = CSVController()

        self.csv_controller.open_folder(folder_path)

        self.button_next.config(state="enabled")

        self.button_replay.config(text="Play again", command=self.play_again)

        self.classification_var.set(self.csv_controller.get_classification(1))

        self.update_button_states()

    def next(self, event=None) -> None:
        """Moves to the next audio file and updates the classification.

        Args:
            event: The event that triggered the method (default: None).
        """
        if self.is_shift_pressed:
            self.prev()
            return

        if self.allow_next:
            self.csv_controller.set_classification(
                self.audio_queue.current_index, self.classification_var.get()
            )
            threading.Thread(target=self.audio_queue.next).start()
            self.classification_var.set(
                self.csv_controller.get_classification(self.audio_queue.current_index)
            )
        self.update_button_states()

    def prev(self, event=None) -> None:
        """Moves to the previous audio file and updates the classification.

        Args:
            event: The event that triggered the method (default: None).
        """
        if self.allow_prev:
            self.csv_controller.set_classification(
                self.audio_queue.current_index, self.classification_var.get()
            )
            threading.Thread(target=self.audio_queue.prev).start()
            self.classification_var.set(
                self.csv_controller.get_classification(self.audio_queue.current_index)
            )

        self.update_button_states()

    def play_again(self) -> None:
        """Plays the current audio file again."""
        threading.Thread(target=self.audio_queue.play_current).start()

    def update_button_states(self) -> None:
        """Updates the state (enabled or disabled) of the navigation buttons."""
        logging.info(f"Current index: {self.audio_queue.current_index}")

        self.allow_prev = self.audio_queue.current_index > 1

        self.allow_next = self.audio_queue.current_index < len(
            self.audio_queue.audio_list
        )

        self.button_next.config(state="enabled" if self.allow_next else "disabled")
        self.button_prev.config(state="enabled" if self.allow_prev else "disabled")

        self.update()
