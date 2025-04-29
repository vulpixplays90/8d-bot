def effectSlowedDown(sound, settings):
    """
    Slows down the audio using user's speedMultiplier setting.
    """
    speedMultiplier = settings["speedMultiplier"]

    soundSlowedDown = sound._spawn(
        sound.raw_data,
        overrides={"frame_rate": int(sound.frame_rate * speedMultiplier)},
    )
    soundSlowedDown.set_frame_rate(sound.frame_rate)
    return soundSlowedDown
