import math
import os
import sys
import subprocess
import speech_recognition as sr

# The current WIT max duration per request is 20 seconds and
# the current API rate limit per user is 240 requests per second
# If any API error should occur, consult rate limit in the 
# WIT FAQ -> RATE LIMIT section: https://wit.ai/faq

# Key can be found under your WIT app settings -> server access token
WIT_AI_KEY = "YOUR_KEY_HERE"

# Duration should be below max possible duration in seconds
CHUNK_DURATION = 15

def main():

    # Check arguments
    if len(sys.argv) != 2:
        print("Usage: python transcribe.py filename.mp4")
        exit(1)
    elif not os.path.isfile(sys.argv[1]):
        print("File specified doesn't exist")
        exit(1)

    # Store filename and file chunks
    print("Extracting file duration")
    INPUT_FILE = sys.argv[1]
    SECONDS = get_seconds(INPUT_FILE)
    CHUNKS = math.ceil(SECONDS / CHUNK_DURATION)

    # Temporarily create a separate audio file
    print("Converting input file to audio")
    CONVERTED_FILE = convert_file(INPUT_FILE)

    # Store transcription in string
    text = ""

    # Parse each chunk separately
    for chunk in range(CHUNKS):
        print("Transcribing... Current chunk: {}/{}".format(chunk + 1, CHUNKS), end="\r")
        chunk_name = create_chunk(CONVERTED_FILE, chunk)
        text += transcribe_chunk(chunk_name, chunk)
        text += "\n"
        os.remove(chunk_name)

    # Delete temporary audio file
    os.remove(CONVERTED_FILE)

    # Export text file
    text_file_name = "{}_transcription.txt".format(os.path.splitext(INPUT_FILE)[0])
    with open(text_file_name, "w") as file:
        file.write(text)

    print("")
    print("Transcription complete!")

def get_seconds(filename):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                             "format=duration", "-of",
                             "default=noprint_wrappers=1:nokey=1", filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)

    # Return video length in seconds rounded up
    return math.ceil(float(result.stdout))

def convert_file(filename):
    output_filename = "temporary_audio_file.mp3"

    # convert file to mp3 with ffmpeg to improve processing speed
    subprocess.call(['ffmpeg', '-i', filename, output_filename, '-loglevel', 'quiet'])

    return output_filename

def create_chunk(filename, chunk):
    # Create current chunk parameters
    chunk_name = "{}.flac".format(chunk + 1)
    start = "{}".format(chunk * CHUNK_DURATION)
    end = "{}".format(CHUNK_DURATION * (chunk + 1))

    # convert file fragment with ffmpeg
    subprocess.call(['ffmpeg', '-i', filename, '-ss', start, '-to', end, 
                     '-c:a', 'flac', chunk_name, '-loglevel', 'quiet'])

    return chunk_name

def transcribe_chunk(filename, chunk):
    # Create recognizer instance
    r = sr.Recognizer()

    # Load chunk
    audio_file = sr.AudioFile(filename)

    # Load audio to recognizer
    with audio_file as source:
        audio = r.record(source)

    # Process file
    try:
        # Use google speech recognition, for more options check
        # the documentation: https://pypi.org/project/SpeechRecognition/
        # (most other options require creating accounts)
        text = r.recognize_wit(audio, key=WIT_AI_KEY)
    except sr.UnknownValueError:
        text = "Inaudible on chunk {}".format(chunk + 1)
    except sr.RequestError as e:
        text = "API error on chunk {}".format(chunk + 1)

    return text

if __name__ == "__main__":
    main()
