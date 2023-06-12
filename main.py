import logging
from tkinter import Tk, ttk, Frame
from classify_audio_chunks import ClassifyAudioChunks
from audio_chunk_generator import AudioChunkGenerator


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[logging.FileHandler("app.log"), logging.StreamHandler()],
)


class MainApplication(Tk):
    """The main application window for the Audio Crop GUI."""

    def __init__(self) -> None:
        """Initialize the MainApplication."""
        logging.info("Initializing MainApplication")
        Tk.__init__(self)

        self.title("Audio Crop")
        self.geometry("800x300")
        self.resizable(False, False)

        # creating a container for all the frames
        container = Frame(self, bg="white")

        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)

        container.pack(side="top", fill="both", expand=True)

        navigation_bar = Frame(self, bg="grey")

        navigation_bar.columnconfigure(0, weight=1)
        navigation_bar.columnconfigure(1, weight=0)
        navigation_bar.columnconfigure(2, weight=0)
        navigation_bar.columnconfigure(3, weight=0)

        navigation_bar.rowconfigure(0, weight=1)

        navigation_bar.pack(side="top", fill="x")

        button_classify = ttk.Button(
            navigation_bar,
            text="Classify Audio",
            command=lambda: self.show_frame(ClassifyAudioChunks),
        )
        button_classify.grid(row=0, column=3, padx=5, pady=10, sticky="e")

        button_split = ttk.Button(
            navigation_bar,
            text="Split Audio",
            command=lambda: self.show_frame(AudioChunkGenerator),
        )
        button_split.grid(row=0, column=2, padx=5, pady=10, sticky="e")

        button_main = ttk.Button(
            navigation_bar, text="Main Page", command=lambda: self.show_frame(MainPage)
        )
        button_main.grid(row=0, column=1, padx=5, pady=10, sticky="e")

        # initializing frames to an empty array
        self.frames = {}

        # iterating through a tuple consisting
        # of the different page layouts
        # Initialize frame of this object from startpage page1 page2.
        for F in (MainPage, AudioChunkGenerator, ClassifyAudioChunks):
            frame = F(container, self)

            # initializing frame of that object from
            # startpage, page1, page2 respectively with
            # for loop
            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(MainPage)
        logging.info("MainApplication initialized successfully")

    def show_frame(self, controller) -> None:
        """Raise the specified frame to the top.

        Args:
            controller: The frame to be raised.
        """
        logging.info(f"Showing frame: {controller.__name__}")
        frame = self.frames[controller]
        frame.tkraise()


class MainPage(Frame):
    """The main page of the Audio Crop application."""

    def __init__(self, parent, controller=None) -> None:
        """Initialize the MainPage.

        Args:
            parent: The parent widget.
            controller: The controller object.
        """
        logging.info("Initializing MainPage")
        Frame.__init__(self, parent)
        main_menu = ttk.Label(
            self, text="Main Page", font=("Helvetica", 18), padding=10
        )
        main_menu.pack()
        logging.info("MainPage initialized successfully")


app = MainApplication()
app.mainloop()
