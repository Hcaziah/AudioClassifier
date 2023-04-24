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
        container.pack(side="top", fill="both", expand=True)

        menu_bar = Menu(self)

        file_menu = Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Open")
        file_menu.add_command(label="Save")
        file_menu.add_command(label="Save as...")
        file_menu.add_command(label="Close")

        edit_menu = Menu(menu_bar, tearoff=0)
        edit_menu.add_command(label="Undo")
        edit_menu.add_command(label="Redo")

        menu_bar.add_cascade(label="File", menu=file_menu)
        menu_bar.add_cascade(label="Edit", menu=edit_menu)
        menu_bar.add_cascade(label="Help")

        self.config(menu=menu_bar)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        navigation_bar = Frame(self, bg="grey")
        navigation_bar.pack(side='bottom', fill='x', anchor='s')

        splitButton = ttk.Button(
            navigation_bar, text="Split Audio", command=lambda: self.show_frame(SplitAudio))
        splitButton.pack(side='right', padx=10, pady=10)

        classifyButton = ttk.Button(
            navigation_bar, text="Classify Audio", command=lambda: self.show_frame(ClassifyAudio))
        classifyButton.pack(side='right', padx=10, pady=10)

        mainButton = ttk.Button(
            navigation_bar, text="Main Page", command=lambda: self.show_frame(MainPage))
        mainButton.pack(side='right', padx=10, pady=10)

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

    def show_frame(self, cont, title=None):
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

        # Add a split audio button
        self.split_audio_button = ttk.Button(
            self, text="Split Audio", command=self.start_split_audio_thread, state="disabled")
        self.split_audio_button.pack(side='bottom', fill='x', padx=10, pady=10)

        # Add output folder frame
        out_dir_frame = Frame(self)
        out_dir_frame.pack(side='bottom', fill="x", padx=10)

        output_dir_button = ttk.Button(
            out_dir_frame, text="Output Folder", command=self.open_folder, width=15)
        output_dir_button.pack(side='right', padx=2, pady=10)

        # Add a output folder dir path label
        out_dir_label = ttk.Label(
            out_dir_frame, text="Output Folder:", width=15)
        out_dir_label.pack(side='left', padx=2, pady=10)

        self.out_path_var = StringVar(out_dir_frame)
        self.out_path_label = ttk.Entry(
            out_dir_frame, text=self.out_path_var, state="readonly")
        self.out_path_label.pack(fill='x', padx=2, pady=10)

        # Add frame for dirs
        in_dir_frame = Frame(self)
        in_dir_frame.pack(side='bottom', fill="x", padx=10)

        # Add a input file button
        input_file_button = ttk.Button(
            in_dir_frame, text="Open File", command=self.open_file, width=15)
        input_file_button.pack(side='right', padx=2, pady=10)

        # Add a dir path label
        dir_label = ttk.Label(in_dir_frame, text="Audio File:", width=15)
        dir_label.pack(side='left', padx=2, pady=10)

        self.in_path_var = StringVar(in_dir_frame)
        self.path_label = ttk.Entry(
            in_dir_frame, text=self.in_path_var, state="readonly")
        self.path_label.pack(fill='x', padx=2, pady=10)

    def open_file(self):
        self.audio_file = filedialog.askopenfilename(initialdir=".", title="Select Audio File", filetypes=(
            ("mp3 files", "*.mp3"), ("wav files", "*.wav"), ("all files", "*.*")))
        self.in_path_var.set(self.audio_file)

        if (self.out_path_var.get() != "" and self.in_path_var.get() != ""):
            self.split_audio_button.config(state='normal')
        else:
            self.split_audio_button.config(state='disabled')

    def open_folder(self):
        self.output_folder = filedialog.askdirectory(
            initialdir='.', title="Select Output Folder")
        self.out_path_var.set(self.output_folder)
        if (self.out_path_var.get() != "" and self.in_path_var.get() != ""):
            self.split_audio_button.config(state='normal')
        else:
            self.split_audio_button.config(state='disabled')

    def start_split_audio_thread(self):
        self.split_audio_thread = threading.Thread(target=self.split_audio)
        self.split_audio_thread.start()

    def split_audio(self):
        folder_name = self.audio_file.split("/")[-1].split(".")[0]

        pathlib.Path(self.out_path_var.get() + "/" + folder_name).mkdir(
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
                f"{self.out_path_var.get()}/{folder_name}/chunk{i}.mp3")

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
