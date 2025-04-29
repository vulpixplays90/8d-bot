import soundfile as sf
from os import remove as removeFile
from pydub import AudioSegment

def saveSound(sound, sampleRate, filename):
    """
    Save the sound in MP3 format using a given filename.
    """
    wav_path = filename.replace(".mp3", ".wav")

    with sf.SoundFile(
        wav_path,
        "w",
        samplerate=sampleRate,
        channels=sound.shape[1],
    ) as f:
        f.write(sound)

    AudioSegment.from_wav(wav_path).export(filename, format="mp3")
    removeFile(wav_path)
