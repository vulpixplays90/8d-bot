
def panArray(settings):
    panBoundary = settings["panBoundary"]
    jumpPercentage = settings["jumpPercentage"]
    timeLtoR = settings["timeLtoR"]

    piecesCtoR = panBoundary / jumpPercentage
    piecesLtoR = piecesCtoR * 2
    pieceTime = int(timeLtoR / piecesLtoR)

    pan = []
    left = -panBoundary
    while left <= panBoundary:
        pan.append(left)
        left += jumpPercentage

    pan = [x / 100 for x in pan]
    return pan, pieceTime

def effect8d(sound, settings):
    volumeMultiplier = settings["volumeMultiplier"]
    panBoundary = settings["panBoundary"]

    pan, pieceTime = panArray(settings)

    sound8d = sound[0]
    panIndex = 0
    iteratePanArrayForward = True

    for time in range(0, len(sound) - pieceTime, pieceTime):
        piece = sound[time : time + pieceTime]

        if panIndex == 0:
            iteratePanArrayForward = True
        if panIndex == len(pan) - 1:
            iteratePanArrayForward = False

        volAdjust = volumeMultiplier - (
            abs(pan[panIndex]) / (panBoundary / 100) * volumeMultiplier
        )
        piece -= volAdjust
        pannedPiece = piece.pan(pan[panIndex])

        panIndex += 1 if iteratePanArrayForward else -1
        sound8d = sound8d + pannedPiece

    return sound8d
