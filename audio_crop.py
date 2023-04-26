from pydub import AudioSegment
from pydub.silence import split_on_silence
from tkinter import Tk, ttk, filedialog, Frame, StringVar, Menu
import threading
import pathlib


class MainApplication(Tk):
    def __init__(self):
        Tk.__init__(self)

        self.title("Audio Crop")
        self.geometry("800x300")

        # creating a container
        container = Frame(self, bg="white")

        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)

        container.pack(side="top", fill="both", expand=True)

        menu_bar = Menu(self)

        file_menu = Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Open")
        file_menu.add_command(label="Save")
        file_menu.add_command(label="Save as...")
        file_menu.add_command(label="Exit", command=self.quit)

        edit_menu = Menu(menu_bar, tearoff=0)
        edit_menu.add_command(label="Undo")
        edit_menu.add_command(label="Redo")
        
        help_menu = Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="About")

        menu_bar.add_cascade(label="File", menu=file_menu)
        menu_bar.add_cascade(label="Edit", menu=edit_menu)
        menu_bar.add_cascade(label="Help", menu=help_menu)

        self.config(menu=menu_bar)

        navigation_bar = Frame(self, bg="grey")
        
        navigation_bar.columnconfigure(0, weight=1)
        navigation_bar.columnconfigure(1, weight=0)
        navigation_bar.columnconfigure(2, weight=0)
        navigation_bar.columnconfigure(3, weight=0)
        
        navigation_bar.rowconfigure(0, weight=1)
        
        navigation_bar.pack(side="top", fill="x")

        button_split = ttk.Button(
            navigation_bar, text="Split Audio", command=lambda: self.show_frame(SplitAudio))
        button_split.grid(row=0, column=2, padx=5, pady=10, sticky="e")

        button_classify = ttk.Button(
            navigation_bar, text="Classify Audio", command=lambda: self.show_frame(ClassifyAudio))
        button_classify.grid(row=0, column=3, padx=5, pady=10, sticky="e")

        button_main = ttk.Button(
            navigation_bar, text="Main Page", command=lambda: self.show_frame(MainPage))
        button_main.grid(row=0, column=1, padx=5, pady=10, sticky="e")
        
        # initializing frames to an empty array
        self.frames = {}

        # iterating through a tuple consisting
        # of the different page layouts
        for F in (MainPage, SplitAudio, ClassifyAudio):
            frame = F(container, self)

            # initializing frame of that object from
            # startpage, page1, page2 respectively with
            # for loop
            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(MainPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class MainPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        mainMenu = ttk.Label(self, text="Main Page", font=("Helvetica", 18))
        mainMenu.pack()


class SplitAudio(Frame):
    def __init__(self, parent, controller) -> None:
        Frame.__init__(self, parent)

        # Set up the main grid
        self.columnconfigure(0, weight=1)

        self.rowconfigure(0, weight=3, minsize=100)
        self.rowconfigure(1, weight=1, minsize=50)
        self.rowconfigure(2, weight=1)

        infoFrame = Frame(self)

        infoFrame.columnconfigure(0, weight=1)
        infoFrame.columnconfigure(1, weight=1)

        infoFrame.rowconfigure(0, weight=1)
        infoFrame.rowconfigure(1, weight=1)

        ##################
        # FILE I/O FRAME #
        ##################
        ioFrame = Frame(self)

        ioFrame.columnconfigure(0, weight=0)
        ioFrame.columnconfigure(1, weight=1)
        ioFrame.columnconfigure(2, weight=0)

        ioFrame.rowconfigure(0, weight=1)
        ioFrame.rowconfigure(1, weight=1)

        ioFrame.grid(row=1, column=0)

        button_output_select = ttk.Button(
            ioFrame, text="Output Folder", command=self.open_folder, width=15)
        button_output_select.grid(row=1, column=2, padx=10, pady=10)

        # Add a output folder dir path label
        label_output_path = ttk.Label(
            ioFrame, text="Output Folder:", width=15)
        label_output_path.grid(row=1, column=0, padx=10, pady=10)

        self.string_output_path = StringVar(ioFrame)

        self.entry_output_path = ttk.Entry(
            ioFrame, text=self.string_output_path, state="readonly", width=1000)
        self.entry_output_path.grid(row=1, column=1, padx=10, pady=10)

        # Add a input file button
        button_input_select = ttk.Button(
            ioFrame, text="Open File", command=self.open_file, width=15)
        button_input_select.grid(row=0, column=2, padx=10, pady=10)

        # Add a dir path label
        label_input_filename = ttk.Label(ioFrame, text="Audio File:", width=15)
        label_input_filename.grid(row=0, column=0, padx=10, pady=10)

        self.string_input_path = StringVar(ioFrame)

        self.entry_input_path = ttk.Entry(
            ioFrame, text=self.string_input_path, state="readonly", width=1000)
        self.entry_input_path.grid(row=0, column=1, padx=10, pady=10)

        # Add a split audio button
        self.split_audio_button = ttk.Button(self, text="Split Audio", command=self.start_split_audio_thread, state="disabled", width=150)
        self.split_audio_button.grid(row=2, column=0, padx=10, pady=10)

    def open_file(self):
        self.audio_file = filedialog.askopenfilename(initialdir=".", title="Select Audio File", filetypes=(
            ("mp3 files", "*.mp3"), ("wav files", "*.wav"), ("all files", "*.*")))
        self.string_input_path.set(self.audio_file)

        if (self.string_output_path.get() != "" and self.string_input_path.get() != ""):
            self.split_audio_button.config(state='normal')
        else:
            self.split_audio_button.config(state='disabled')

    def open_folder(self):
        self.output_folder = filedialog.askdirectory(
            initialdir='.', title="Select Output Folder")
        self.string_output_path.set(self.output_folder)
        if (self.string_output_path.get() != "" and self.string_input_path.get() != ""):
            self.split_audio_button.config(state='normal')
        else:
            self.split_audio_button.config(state='disabled')

    def start_split_audio_thread(self):
        self.split_audio_thread = threading.Thread(target=self.split_audio)
        self.split_audio_thread.start()

    def split_audio(self):
        folder_name = self.audio_file.split("/")[-1].split(".")[0]

        pathlib.Path(self.string_output_path.get() + "/" + folder_name).mkdir(
            parents=True, exist_ok=True)

        self.split_audio_button.config(
            text="Loading file...", state="disabled")
        self.update()

        audio = AudioSegment.from_file(self.audio_file)

        self.split_audio_button.config(text="Splitting...", state="disabled")
        self.update()

        chunks = split_on_silence(
            audio, min_silence_len=750, silence_thresh=-48)

        self.split_audio_button.config(
            text=f"Exporting {len(chunks)} chunks...", state="disabled")
        self.update()

        for i, chunk in enumerate(chunks):
            silent_chunk = AudioSegment.silent(duration=500)

            audio_chunk = silent_chunk + chunk + silent_chunk

            audio_chunk.export(
                f"{self.string_output_path.get()}/{folder_name}/chunk{i}.mp3")

        self.split_audio_button.config(text="Split Audio", state="normal")
        self.update()


class ClassifyAudio(Frame):
    def __init__(self, parent, controller) -> None:
        Frame.__init__(self, parent)

        self.currentIDX = 0
        self.shiftPressed = False

        # Add buttons
        buttonFrame = Frame(self)
        buttonFrame.pack(side='bottom', fill='x', padx=50, pady=10)
        nextButton = ttk.Button(buttonFrame, text="->",
                                command=self.next, width=5)
        self.buttonPrevious = ttk.Button(
            buttonFrame, text="<-", command=self.prev, width=5)
        playAgainButton = ttk.Button(
            buttonFrame, text="Play again", command=self.playAgain, width=10)

        nextButton.pack(side='right', padx=10)
        self.buttonPrevious.pack(side='left', padx=10)
        playAgainButton.pack(side='bottom', fill='x')

        # Add text box
        self.textbox = ttk.Entry(self, text="Audio File: ")
        self.textbox.pack(side='bottom', fill='x', padx=10, pady=10)

        controller.bind("<Return>", self.next)

        controller.bind("<KeyPress-Shift_L>", self.shift_press)
        controller.bind("<KeyRelease-Shift_L>", self.shift_release)

    def shift_press(self, event):
        self.shiftPressed = True

    def shift_release(self, event):
        self.shiftPressed = False

    def next(self, event=None):
        if self.shiftPressed:
            self.prev()
            return

        self.currentIDX += 1

        if self.currentIDX > 0:
            self.buttonPrevious.config(state='enabled')

    def prev(self, event=None):
        if self.currentIDX > 0:
            self.currentIDX -= 1

        if self.currentIDX == 0:
            self.buttonPrevious.config(state='disabled')

    def playAgain(self):
        pass


app = MainApplication()
app.mainloop()
