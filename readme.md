# Audio Chunk Generator

The Audio Chunk Generator is a GUI application built using the Tkinter library in Python. It allows you to split audio files into smaller chunks based on silence detection. This can be useful for tasks such as transcribing long audio recordings or processing audio files in smaller segments.

## Features

- Select an input audio file in MP3 or WAV format.
- Choose an output folder to save the generated audio chunks.
- Split the audio file into chunks based on silence detection.
- Export the generated chunks as MP3 files.

## Requirements

- Python 3.x
- Tkinter library
- PyDub library

## Installation

1. Clone the repository:

   ```
   git clone https://github.com/your-username/audio-chunk-generator.git
   ```

2. Install the required dependencies:

   ```
   pip install pydub
   ```

## Usage

1. Run the application by executing the `audio_chunk_generator.py` file:

   ```
   python audio_chunk_generator.py
   ```

2. Select an input audio file by clicking the "Open File" button.
3. Choose an output folder by clicking the "Select Output" button.
4. Click the "Split Audio" button to start the audio splitting process.
5. The application will display the progress and status of the splitting process.
6. Once the splitting is complete, the generated audio chunks will be saved in the specified output folder.

## Contributing

Contributions are welcome! If you have any suggestions, bug reports, or feature requests, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

