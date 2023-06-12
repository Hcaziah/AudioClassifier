# AudioClassifier

This program allows ease of classifying audio for training data for machine learning. Also has split by silence functionality for large single audio files.

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
   git clone https://github.com/Hcaziah/AudioClassifier.git
   ```

2. Install the required dependencies:

   ```
   pip install pydub simpleaudio
   ```

## Usage

1. Run the application by executing the `main.py` file:

   ```
   python main.py
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

