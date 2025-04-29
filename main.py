import sys
import numpy as np
from pydub import AudioSegment
from db import get_user_settings
from loadSound import loadSound
from saveSound import saveSound
from effect8d import effect8d
from slow import effectSlowedDown
from reverb import effectReverb

input_file = sys.argv[1]
output_file = sys.argv[2]
chat_id = int(sys.argv[3])

settings = get_user_settings(chat_id)
sound = loadSound(input_file)

# Step 1: Apply 8D and slowdown to the full audio
sound_8d = effect8d(sound, settings)
sound_slowed = effectSlowedDown(sound_8d, settings)

# Step 2: Split into chunks for memory-friendly reverb
chunk_length_ms = 30 * 1000
chunks = [sound_slowed[i:i + chunk_length_ms] for i in range(0, len(sound_slowed), chunk_length_ms)]

final_audio = AudioSegment.empty()

for i, chunk in enumerate(chunks):
    print(f"Reverbing chunk {i + 1}/{len(chunks)}...")
    
    chunk_reverbed, sampleRate = effectReverb(chunk, settings)

    # Ensure stereo
    if len(chunk_reverbed.shape) == 1:
        chunk_reverbed = np.stack([chunk_reverbed, chunk_reverbed], axis=-1)

    chunk_reverbed = np.clip(chunk_reverbed, -1.0, 1.0)
    chunk_int16 = (chunk_reverbed * 32767).astype(np.int16)

    chunk_final = AudioSegment(
        chunk_int16.tobytes(),
        frame_rate=sampleRate,
        sample_width=2,
        channels=2
    )

    final_audio += chunk_final

# Step 3: Save the final file
saveSound(final_audio, sampleRate, output_file)
