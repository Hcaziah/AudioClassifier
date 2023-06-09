from tkinter import Frame, ttk, StringVar, filedialog
import pathlib
import threading
from pydub import AudioSegment
from pydub.silence import split_on_silence
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[logging.FileHandler("app.log"), logging.StreamHandler()],
)


class AudioChunkGenerator(Frame):
    """GUI application for splitting audio files into chunks.

    Attributes:
        audio_file (str): The path to the input audio file.
        output_folder (str): The path to the output folder for the generated audio chunks.
        string_output_path (StringVar): String variable for displaying the output folder path.
        split_audio_thread (threading.Thread): Thread for splitting the audio file.
        split_audio_button (ttk.Button): Button for initiating the audio splitting process.
    """

    def __init__(self, parent, controller=None) -> None:
        """Initializes the AudioChunkGenerator frame.

        Args:
            parent: The parent widget.
            controller: The controller object.
        """
        Frame.__init__(self, parent)
        self.audio_file = None

        self.output_folder = None
        self.string_output_path = StringVar()

        self.split_audio_thread = None

        # Set up the main grid
        self.columnconfigure(0, weight=1)

        self.rowconfigure(0, weight=3, minsize=100)
        self.rowconfigure(1, weight=1, minsize=50)
        self.rowconfigure(2, weight=1)

        ##################
        #   INFO FRAME   #
        ##################
        info_frame = Frame(self)

        checkbox_options = []
        self.checkbox_values = {}

        for option in checkbox_options:
            var = StringVar()
            checkbox = ttk.Checkbutton(
                info_frame, text=option, variable=var, onvalue="on", offvalue="off"
            )

            checkbox.pack()
            self.checkbox_values[option] = var

        info_frame.columnconfigure(0, weight=1)
        info_frame.columnconfigure(1, weight=1)

        info_frame.rowconfigure(0, weight=1)
        info_frame.rowconfigure(1, weight=1)

        ##################
        # FILE I/O FRAME #
        ##################
        io_frame = Frame(self)

        io_frame.columnconfigure(0, weight=0)
        io_frame.columnconfigure(1, weight=1)
        io_frame.columnconfigure(2, weight=0)

        io_frame.rowconfigure(0, weight=1)
        io_frame.rowconfigure(1, weight=1)

        io_frame.grid(row=1, column=0)

        button_output_select = ttk.Button(
            io_frame, text="Select output", command=self.open_folder, width=15
        )
        button_output_select.grid(row=1, column=2, padx=10, pady=10)

        # Add a output folder dir path label
        label_output_path = ttk.Label(io_frame, text="Output Folder:", width=15)
        label_output_path.grid(row=1, column=0, padx=10, pady=10)

        self.string_output_path = StringVar(io_frame)

        self.entry_output_path = ttk.Entry(
            io_frame, text=self.string_output_path, state="readonly", width=1000
        )
        self.entry_output_path.grid(row=1, column=1, padx=10, pady=10)

        # Add a input file button
        button_input_select = ttk.Button(
            io_frame, text="Open File", command=self.open_file, width=15
        )
        button_input_select.grid(row=0, column=2, padx=10, pady=10)

        # Add a dir path label
        label_input_filename = ttk.Label(io_frame, text="Audio File:", width=15)
        label_input_filename.grid(row=0, column=0, padx=10, pady=10)

        self.string_input_path = StringVar(io_frame)

        self.entry_input_path = ttk.Entry(
            io_frame, text=self.string_input_path, state="readonly", width=1000
        )
        self.entry_input_path.grid(row=0, column=1, padx=10, pady=10)

        # Add a split audio button
        self.split_audio_button = ttk.Button(
            self,
            text="Split Audio",
            command=self._start_split_audio_thread,
            state="disabled",
            width=150,
        )
        self.split_audio_button.grid(row=2, column=0, padx=10, pady=10)
        logging.info("AudioChunkGenerator initialized.")

    def open_file(self) -> str:
        """Opens a file dialog to select an audio file."""
        self.audio_file = filedialog.askopenfilename(
            initialdir=".",
            title="Select Audio File",
            filetypes=(
                ("mp3 files", "*.mp3"),
                ("wav files", "*.wav"),
                ("all files", "*.*"),
            ),
        )
        self.string_input_path.set(self.audio_file)

        if self.string_output_path.get() != "" and self.string_input_path.get() != "":
            self.split_audio_button.config(state="normal")
        else:
            self.split_audio_button.config(state="disabled")

    def open_folder(self) -> str:
        """Opens a folder dialog to select the output folder."""
        self.output_folder = filedialog.askdirectory(
            initialdir=".", title="Select Output Folder"
        )

        self.string_output_path.set(self.output_folder)
        if self.string_output_path.get() != "" and self.string_input_path.get() != "":
            self.split_audio_button.config(state="normal")
        else:
            self.split_audio_button.config(state="disabled")

    def _start_split_audio_thread(self) -> None:
        threading.Thread(target=self._split_audio).start()

    def _split_audio(self) -> None:
        folder_name = self.audio_file.split("/")[-1].split(".")[0]

        pathlib.Path(self.string_output_path.get() + "/" + folder_name).mkdir(
            parents=True, exist_ok=True
        )

        self.split_audio_button.config(text="Loading file...", state="disabled")
        self.update()

        audio = AudioSegment.from_file(self.audio_file)

        logging.info(f"Splitting {self.audio_file} into {folder_name}...")
        self.split_audio_button.config(text="Splitting...", state="disabled")
        self.update()

        chunks = split_on_silence(audio, min_silence_len=500, silence_thresh=-48)

        logging.info(f"Exporting {len(chunks)} chunks...")
        self.split_audio_button.config(
            text=f"Exporting {len(chunks)} chunks...", state="disabled"
        )
        self.update()

        for i, chunk in enumerate(chunks):
            silent_chunk = AudioSegment.silent(duration=500)

            audio_chunk = silent_chunk + chunk + silent_chunk

            audio_chunk.export(
                f"{self.string_output_path.get()}/{folder_name}/{str(i).zfill(4)}.mp3"
            )
            logging.info(f"Exported {str(i).zfill(4)}.mp3 to {folder_name}...")

        logging.info(f"Finished exporting {len(chunks)} chunks...")
        self.split_audio_button.config(text="Split Audio", state="normal")
        self.update()
