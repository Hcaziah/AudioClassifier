import os
import threading
from tkinter import Frame, ttk
from IOController import FileController, IOController
import simpleaudio

IOC = IOController()


class AudioQueue:
    def __init__(self, folder_path) -> None:
        self.folder_path = folder_path
        self.current_index = 0
        self.audio_list = []
        self._playback = None

        for file in os.listdir(self.folder_path):
            self.audio_list.append(FileController(
                f'{self.folder_path}\\{file}'))

    def play_current(self):
        segment = self.audio_list[self.current_index].audio_file

        self._playback = simpleaudio.play_buffer(
            segment.raw_data,
            bytes_per_sample=segment.sample_width,
            sample_rate=segment.frame_rate,
            num_channels=segment.channels
        )

    def stop_current(self) -> None:
        print(self._playback)
        if self._playback:
            self._playback.stop()

    def next(self):
        self.stop_current()
        self.current_index += 1
        self.play_current()
        return self.audio_list[self.current_index]

    def prev(self) -> int:
        self.stop_current()
        self.current_index -= 1
        self.play_current()

        return self.audio_list[self.current_index]


class ClassifyAudioChunks(Frame):
    """
    A class for classifying audio files.

    This class represents a GUI interface for classifying audio files. It inherits from the tkinter.Frame
    class and takes two parameters in the constructor: parent and controller.

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

        self.current_index = 0
        self.is_shift_pressed = False

        # Add buttons
        button_frame = Frame(self)
        button_frame.pack(side='bottom', fill='x', padx=50, pady=10)
        self.button_next = ttk.Button(
            button_frame, text="->", command=self.next, width=5)
        self.button_prev = ttk.Button(
            button_frame, text="<-", command=self.prev, width=5)
        self.button_replay = ttk.Button(
            button_frame, text="Play again", command=self.play_again, width=10)

        self.button_next.pack(side='right', padx=10)
        self.button_prev.pack(side='left', padx=10)
        self.button_replay.pack(side='bottom', fill='x')

        # Add text box
        self.textbox = ttk.Entry(self, text="Audio File: ")
        self.textbox.pack(side='bottom', fill='x', padx=10, pady=10)

        controller.bind("<Return>", self.next)

        controller.bind("<KeyPress-Shift_L>",
                        lambda event: setattr(self, 'is_shift_pressed', True))
        controller.bind("<KeyRelease-Shift_L>",
                        lambda event: setattr(self, 'is_shift_pressed', False))

        self.audio_queue = AudioQueue("audio/longtest")

        self.thread = None

        self.update_button_states()

    def next(self):
        """
        Go to the next audio file.

        If the shift key is pressed, it will go to the next unclassified audio file.
        """
        if self.is_shift_pressed:
            self.prev()
            return

        self.update_button_states()
        threading.Thread(target=self.audio_queue.next).start()
        print(self.audio_queue.current_index)

    def prev(self):
        """
        Go to the previous audio file.

        If the shift key is pressed, it will go to the previous unclassified audio file.
        """
        self.update_button_states()
        threading.Thread(target=self.audio_queue.prev).start()
        print(self.audio_queue.current_index)

    def play_again(self):
        """
        Plays the current audio file again.
        """
        threading.Thread(target=self.audio_queue.play_current).start()

    def update_button_states(self):
        """
        Update the state of the 'previous' and 'next' buttons based on the current position in the audio queue.

        This method checks the current index of the audio queue and enables or disables the 'previous' and 'next'
        buttons accordingly. If the current index is at the beginning of the queue, the 'previous' button is disabled.
        If the current index is at the end of the queue, the 'next' button is disabled. The method also calls the
        update() function to refresh the user interface.
        """
        if self.audio_queue.current_index == 0:
            self.button_prev.config(state='disabled')
        else:
            self.button_prev.config(state='enabled')

        if self.audio_queue.current_index > len(self.audio_queue.audio_list) - 2:
            self.button_next.config(state='disabled')
        else:
            self.button_next.config(state='enabled')

        self.update()
