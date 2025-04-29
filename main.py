import sys
from db import get_user_settings  # Import your MongoDB util

from loadSound import loadSound
from saveSound import saveSound
from effect8d import effect8d
from slow import effectSlowedDown
from reverb import effectReverb

input_file = sys.argv[1]
output_file = sys.argv[2]
chat_id = int(sys.argv[3])  # Third argument is the user's chat ID

settings = get_user_settings(chat_id)  # Now we can fetch user-specific settings

sound = loadSound(input_file)
sound8d = effect8d(sound, settings)
sound8dAndSlowedDown = effectSlowedDown(sound8d, settings)
sound8dSlowedDownReverbed, sampleRate = effectReverb(sound8dAndSlowedDown, settings)

saveSound(sound8dSlowedDownReverbed, sampleRate, output_file)
