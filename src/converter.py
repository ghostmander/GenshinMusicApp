gapMap = {
    1: "l",
    2: "j",
    3: "h",
    4: "g",
    6: "f",
    8: "d",
    12: "s",
    16: "a"
}


def findGap(gapNum):
    gapS = ""
    if gapNum in gapMap:
        gapS = gapMap[gapNum]
    else:
        keys = sorted(list(gapMap.keys()), reverse=True)
        while gapNum > 0:
            for key in keys:
                if gapNum >= key:
                    gapNum -= key
                    gapS += gapMap[key]
                    break
    return gapS


def convertABC15(song: str):
    mapping = {
        "C1": 15,
        "C2": 16,
        "C3": 17,
        "C4": 18,
        "C5": 19,
        "B1": 8,
        "B2": 9,
        "B3": 10,
        "B4": 11,
        "B5": 12,
        "A1": 1,
        "A2": 2,
        "A3": 3,
        "A4": 4,
        "A5": 5
    }
    finalSheet = ""
    gap = 0
    beats = song.split()
    for i, beat in enumerate(beats):
        if beat == ".":
            gap += 1
        else:
            if gap > 0:
                finalSheet += f"{findGap(gap)} "
                gap = 0
            currBeat = beat
            for note in mapping:
                currBeat = currBeat.replace(note, f"{mapping[note]} ")
            finalSheet += f"{currBeat}"

    return finalSheet
