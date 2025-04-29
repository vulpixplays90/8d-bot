import soundfile as sf
from pedalboard import Pedalboard, Reverb
import tempfile

def tempAudioFile(sound):
    """
    Pedalboard requires a file-based WAV format, so we write to a temp file.
    """
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_wav:
        sound.export(temp_wav.name, format="wav")
        audio, sampleRate = sf.read(temp_wav.name)
    return audio, sampleRate

def effectReverb(sound, settings):
    """
    Adds reverb effect using user-specific reverb parameters.
    """
    reverb_settings = settings["reverb"]
    sound, sampleRate = tempAudioFile(sound)

    addReverb = Pedalboard([
        Reverb(
            room_size=reverb_settings.get("room_size", 0.8),
            damping=reverb_settings.get("damping", 1),
            width=reverb_settings.get("width", 0.5),
            wet_level=reverb_settings.get("wet_level", 0.3),
            dry_level=reverb_settings.get("dry_level", 0.8),
        )
    ])

    reverbedSound = addReverb(sound, sample_rate=sampleRate)
    return reverbedSound, sampleRate
