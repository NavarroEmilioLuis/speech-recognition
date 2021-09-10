# Speech to text
A simple script to transcribe speech from a video file to a text file using Wit.ai for speech recognition.

## Requirements

- Python 3.7.9
- pip 21.0.1
- ffmpeg 4.4

## Setup

- Install python, pip and ffmpeg (see notes).
- Create a wit.ai account, app and intent (see notes).
- Inside the folder, run `pip install -r requirements.txt` to install the dependencies.
- Add the video files that you want to transcribe to the folder.

## Usage

Add your API key into the file transcribe.py.
Run `python transcribe.py filename.mp4` and it will export a .txt file with the transcription.

## Notes

### FFMPEG
Installing ffmpeg depends on your specific OS. The easiest way is to use an installer (Chocolatey, Homebrew, Apt).

### WIT.AI
From SpeechRecognition docs:

>You will need to add at least one intent to the app before you can see the API key, though the actual intent settings don't matter.

>To get the API key for a Wit.ai app, go to the app's overview page, go to the section titled "Make an API request", and look for something along the lines of Authorization: Bearer XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX; XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX is the API key. Wit.ai API keys are 32-character uppercase alphanumeric strings.
