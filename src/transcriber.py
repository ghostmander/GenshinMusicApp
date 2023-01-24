from src.songs import songSheet
from src.converter import convertABC15
# Rules:
# 1-21 are keys.
# >   1- 7 = [Z, X, C, V, B, N, M]
# >   8-14 = [A, S, D, F, G, H, J]
# >  15-21 = [Q, W, E, R, T, Y, U]
#
# letters are spacing (in 16th of a beat [240/bpm * letter/16]):
# Delay = bpm / 3840 * letter
# > l = 1
# > j = 2
# > h = 3
# > g = 4
# > f = 6
# > d = 8
# > s = 12
# > a = 16
#
# moreoever, the following are special keys:
# n = 25ms delay
# ö = 50ms delay

bindings = {
    "1": "z",
    "2": "x",
    "3": "c",
    "4": "v",
    "5": "b",
    "6": "n",
    "7": "m",
    "8": "a",
    "9": "s",
    "10": "d",
    "11": "f",
    "12": "g",
    "13": "h",
    "14": "j",
    "15": "q",
    "16": "w",
    "17": "e",
    "18": "r",
    "19": "t",
    "20": "y",
    "21": "u",

    "l": 1,
    "j": 2,
    "h": 3,
    "g": 4,
    "f": 6,
    "d": 8,
    "s": 12,
    "a": 16,


    # "l": 0.0625,
    # "j": 0.125,
    # "h": 0.1875,
    # "g": 0.25,
    # "f": 0.375,
    # "d": 0.5,
    # "s": 0.75,
    # "a": 1.0,
}
specialDelay = {
    "n": 0.025,
    "ö": 0.050
}


def songParser(songNotes: str, encoding: str = "default"):
    if encoding != "default":
        if encoding == "ABC[1-5]":
            songNotes = convertABC15(songNotes)
        else:
            return
    songNotes = songNotes.replace("  ", " l ")
    parsedSong = []
    for key in songNotes.split():
        if key in bindings:
            parsedSong.append(bindings[key])
        elif key in specialDelay:
            parsedSong.append(specialDelay[key])
        else:
            if key.isalpha() and all(letter in bindings for letter in key):
                delay = 0
                for letter in key:
                    delay += bindings[letter]
                parsedSong.append(delay)
            else:
                print("\033[93mWarning: \033[0mUnknown key: " + key)
    return parsedSong


if __name__ == "__main__":
    # Test
    print("Song: ", songParser(
        songSheet["Alhaitham demo"]["notes"] + "  1 k |"))
