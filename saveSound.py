from pydub import AudioSegment
import os

def saveSound(sound: AudioSegment, sampleRate: int, filename: str):
    """
    Save the final AudioSegment to an MP3 file.
    """
    os.makedirs(os.path.dirname(filename), exist_ok=True) if os.path.dirname(filename) else None
    sound.export(filename, format="mp3")
