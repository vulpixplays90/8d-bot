from pydub import AudioSegment
import os
import sys
import subprocess

def loadSound(music_file):
    print(f"Attempting to load: {music_file}")
    if music_file.endswith(".mp3") or music_file.endswith(".wav"):
        try:
            sound = AudioSegment.from_file(music_file)
            return sound
        except Exception as e:
            print(f"Error loading audio file: {e}")
            print("Trying to auto-repair using ffmpeg...")

            # Auto-repair using ffmpeg
            repaired_file = f"repaired_{music_file}"
            command = [
                "ffmpeg",
                "-y",  # Overwrite if exists
                "-i", music_file,
                "-codec:a", "libmp3lame",
                repaired_file
            ]
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if result.returncode != 0:
                print("FFmpeg repair failed:")
                print(result.stderr.decode())
                sys.exit(1)

            print("Repair succeeded. Retrying load...")

            try:
                sound = AudioSegment.from_file(repaired_file)
                return sound
            except Exception as e2:
                print(f"Failed to load even after repair: {e2}")
                sys.exit(1)
    else:
        print("Invalid file type. Please use mp3 or wav.")
        sys.exit(1)
