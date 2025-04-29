from pydub import AudioSegment
from os.path import isfile
import sys

def loadSound(filename):
    """
    Loads and returns the MP3 or WAV source sound file.
    """
    if isfile(filename):
        if filename.endswith(".mp3"):
            return AudioSegment.from_mp3(filename)
        elif filename.endswith(".wav"):
            return AudioSegment.from_wav(filename)
    print("Source music file not found!")
    sys.exit(1)
