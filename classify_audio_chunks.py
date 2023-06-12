import os
import threading
from tkinter import Frame, ttk, filedialog, StringVar
import simpleaudio
from file_controller import FileController
from csv_controller import CSVController


class AudioQueue:
    """
    A class for managing a queue of audio files.
    """

    def __init__(self, folder_path=None) -> None:
        self.folder_path = folder_path
        self.current_index = 1
        self.audio_list = []
        self._playback = None

        for file in os.listdir(self.folder_path):
            if file.endswith(".csv"):
                continue

            self.audio_list.append(FileController(f"{self.folder_path}\\{file}"))

    def play_current(self) -> None:
        """
        play_current is a method that plays the current audio file.
        """
        segment = self.audio_list[self.current_index - 1].audio_file

        self._playback = simpleaudio.play_buffer(
            segment.raw_data,
            bytes_per_sample=segment.sample_width,
            sample_rate=segment.frame_rate,
            num_channels=segment.channels,
        )

    def stop_current(self) -> None:
        """
        stop_current is a method that stops the current audio file.
        """
        if self._playback:
            self._playback.stop()

    def next(self) -> None:
        """
        next is a method that goes to the next audio file.
        """
        self.stop_current()
        self.current_index += 1
        self.play_current()

    def prev(self) -> int:
        """
        prev is a method that goes to the previous audio file.
        """
        self.stop_current()
        self.current_index -= 1
        self.play_current()


class ClassifyAudioChunks(Frame):
    """
    A class for classifying audio files.

    This class represents a GUI interface for classifying audio files. It inherits from the
    tkinter.Frame class and takes two parameters in the constructor: parent and controller.

    Attributes
    ----------
    current_index : int
        The index of the current audio file.
    is_shift_pressed : bool
        Whether the shift key is currently pressed.
    textbox : tkinter.Entry
        The textbox for entering the audio file name.

    Methods
    -------
    next()
        Goes to the next audio file.
    prev()
        Goes to the previous audio file.
    play_again()
        Plays the current audio file again.
    """

    def __init__(self, parent, controller=None) -> None:
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

        self.classification_var = ttk.Entry(self, textvariable=self.classification_var)
        self.classification_var.pack(side="bottom", fill="x", padx=10, pady=10)

        self.button_prev.config(state="disabled")
        self.button_next.config(state="disabled")

    def open_folder(self) -> None:
        """
        Opens a folder and starts classifying the audio files in it.
        """
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

        self.audio_queue = AudioQueue(folder_path)
        self.csv_controller = CSVController()

        self.csv_controller.open_folder(folder_path)

        self.button_next.config(state="enabled")

        self.button_replay.config(text="Play again", command=self.play_again)

        self.classification_var.set(self.csv_controller.get_classification(1))

        self.update_button_states()

    def next(self, event=None) -> None:
        """
        next is a method that goes to the next audio file.

        If the shift key is pressed, it will go to the next audio file.
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
        """
        Go to the previous audio file.
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
        """
        Plays the current audio file again.
        """
        threading.Thread(target=self.audio_queue.play_current).start()

    def update_button_states(self) -> None:
        """
        Update the state of the 'previous' and 'next' buttons based on the current position in
        the audio queue.

        This method checks the current index of the audio queue and enables or disables the
        'previous' and 'next' buttons accordingly.
        If the current index is at the beginning of the queue, the 'previous' button is disabled.
        If the current index is at the end of the queue, the 'next' button is disabled.
        The method also calls the update() function to refresh the user interface.
        """
        print(self.audio_queue.current_index)

        self.allow_prev = self.audio_queue.current_index > 1

        self.allow_next = self.audio_queue.current_index < len(
            self.audio_queue.audio_list
        )

        self.button_next.config(state="enabled" if self.allow_next else "disabled")
        self.button_prev.config(state="enabled" if self.allow_prev else "disabled")

        self.update()
