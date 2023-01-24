from typing import TypedDict
from converter import convertABC15
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


class Song(TypedDict):
    Name: str
    BPM: int
    notes: str


songSheet: dict[str: Song] = {
    "Alhaitham demo": {
        "Name": "Alhaitham demo song",
        "BPM": 512,
        "Encoding": "default",
        "notes": "l 8 2 h 9 l 2 j 11 l 2 l 8 h 9 l 2 j 6 j 8 2 h 9 l 2 j 11 l 2 l 13 h 9 l 2 j 8 j 8 2 h 9 l 2 j 11 l 2 l 8 h 9 l 2 j 6 j 8 2 h 9 l 2 l 11 j 9 d l 10 1 h 2 h 8 4 j 1 h 2 h 2 j 1 h 2 h 4 j 4 7 h 8 2 h 1 7 j 1 h 2 h 4 6 j 1 h 2 h 2 j 1 h 2 h 4 j 6 h 2 h 1 j 10 1 h 2 h 8 4 j 1 h 2 h 2 j 1 h 2 h 12 4 j 6 j 11 l 2 h 10 1 j 14 1 h 2 h 15 4 j 1 h 2 l 14 j 2 j 1 j 13 l 2 j 4 j 2 f l 16 l 17 l 18 2 j 2 l 17 l 6 j 18 2 j 13 2 j 2 j 6 j 2 j 18 1 j 1 l 17 l 6 j 18 1 j 13 1 j 1 j 6 j 18 1 l 19 l 20 4 j 4 l 20 l 8 j 20 4 j 20 4 j 4 l 19 l 8 j 18 4 j 19 5 j 5 j 9 j 16 5 j 5 j 5 j 9 j 16 5 j 20 5 j 5 j 9 j 16 5 j 5 j 5 j 9 j 18 5 j 17 6 j 6 l 15 l 10 j 12 6 j 6 j 15 6 j 16 10 j 17 6 j 17 5 j 5 j 9 j 16 5 j 16 5 j 5 j 9 j 5 j 19 3 h 3 l 16 j 3 j 17 6 h 6 h 9 6 l 10 l 11 2 h 10 l 6 j 11 j 2 6 g 6 j 9 l 10 l 11 2 h 10 l 6 j 11 j 2 6 g 6 j 11 l 12 l 13 4 g 8 j 13 j 13 4 h 14 l 8 j 15 j 14 5 g 9 j 12 j 5 g 9 j 9 j 13 5 f 9 d 10 l 11 l 12 1 h 11 1 h 10 1 j 12 1 h 15 h 17 j 17 2 f 16 a j 7 h 8 h 7 j 2 f 6 a d j 10 2 f 8 a 12 g 11 g 10 j 14 2 f 15 f 14 f 13"
    },
    "Sweater Weather": {
        "Name": "Sweater Weather",
        "BPM": 210,
        "Encoding": "ABC[1-5]",
        "notes": "B4 . . . . . B3 . . . . . B5 . . . A1A4B1 . . . . . . . . . . . . . . . A1A4B1B4 . . . . . B3 . . . . . B5 . . . A1A4B1 . . . . . . . . . . . B3 . . . A1A4B1B4 . . . . . . . B3 . . . B5 . . . A1A3B1 . . . . . . . . . . . . . . . A1A3B1B4 . . . . . . . B5 . . . B4 . . . A1A3A5 . . . . . . . . . . . B3 . . . A1A3A5B4 . . . . . . . B3 . . . B5 . . . A1A4B1 . . . . . . . . . . . . . . . A1A4B1B4 . . . . . B3 . . . . . B5 . . . A1A4B1 . . . . . . . . . . . B3 . . . A1A4B1B4 . . . . . . . B5 . . . B4 . . . A1A3B1 . . . B3 . . . B1 . . . B3 . . . A1A3B1B4 . . . . . B3 . B1 . . . B4 . . . A1A3A5 . . . . . . . B1 . . . B3 . . . A1A3A5B4 . . . B4 . . . B3 . . . B4 . . . A1A4B1B4 . . . . . . . . . . . B1 . . . A1A4B1B5 . . . B4 . . . B4 . . . B4 . . . A1A4B1 . . . B3 . . . . . . . . . . . A1A4B1B4 . . . B4 . . . B4 . . . B4 . . . A1A3B1 . . . . . . . B4 . . . B3 . . . A1A3B1B4 . . . B4 . . . B3 . . . B4 . . . A1A3A5B5 . . . . . . . . . . . . . . . A1A3A5B5 . . . . . . . B5 . . . . . . . A1A4B1B5 . . . . . . . . . . . B3 . . . A1A4B1B3 . . . . . C2 . . . . . B5 . . . A1A4B1 . . . . . . . . . . . . . . . A1A4B1B5 . . . B4 . . . B5 . . . . . . . A1A3B1B5 . . . B4 . . . B5 . . . . . . . A1A3B1B5 . . . . . . . B5 . . . . . . . A1A3A5B4 . . . . . . . . . . . . . . . A1A3A5B3 . . . . . . . B1 . . . . . . . A1A4B1 . . . B4 . . . B4 . . . B4 . B3 . A1A4B1B4 . . . B3 . B3 . . . . . . . . . A1A3A5 . . . . . . . . . B3 . B4 . B3 . A1A3A5B4 . . . B5 . B5 . . . . . . . . . A1A3B1 . . . B5 . . . B4 . . . . . . . A1A3B1 . . . B3 . . . B3 . . . . . . . A1A3A5 . . . B5 . . . B4 . . . . . . . A1A3A5 . . . B3 . . . B3 . . . . . . . A1A4B1 . . . B4 . . . B5 . . . . . . . A1A4B1 . . . B3 . . . B3 . . . . . . . A1A3A5 . . . B4 . . . B4 . . . . . . . A1A3A5 . . . B3 . . . B3 . . . . . . . A1A3B1B4 . B3 . B4 . . . B4 . B3 . B4 . B3 . A1A3B1B4 . . . B3 . . . B3 . . . B5 . . . A1A3A5 . . . . . . . . . . . B3 . . . A1A3A5B4 . . . . . . . B3 . . . . . . . A1A4B1B4 . . . B5 . . . B4 . . . B3 . . . B1 . . . . . . . C1 . . . . . . . A3B1B3B5 . . . . . . . . . . . . . . . B1 . . . . . . . C1 . . . . . . . A1A3B1B5 . . . . . . . . . . . . . . . . . . . . . . . . . . . B3 . . . A1A3A5B4 . . . . . . . . . . . B3 . . . B4 . . . . . . . B3 . . . . . . . A1A4B1B4 . . . B5 . . . B4 . . . B3 . . . B1 . . . . . . . C1 . . . . . . . A3B1B3B5 . . . . . . . . . . . . . . . B1 . . . . . . . C1 . . . . . . . A1A3B1B5 . . . . . . . . . . . B4 . . . . . . . . . . . . . . . B3 . . . A1A3A5B2 . . . . . . . B2 . . . B1 . . . B2 . . . B3 . . . . . . . B3 . . . A1A4B1B5 . . . B4 . . . B4 . . . B4 . . . A1A4B1B4 . . . B3 . B1 . . . . . . . . . A1A4B1B4 . B3 . B4 . . . B4 . B3 . B4 . . . A1A4B1B4 . . . B3 . B1 . . . . . . . B4 . A1A3B1 . B4 . . . B3 . B4 . . . B4 . . . A1A3B1B4 . . . B3 . B4 . . . . . . . B3 . A1A3A5B4 . . . B4 . B3 . B4 . . . B4 . . . A1A3A5B4 . . . B3 . B1 . . . . . . . . . A1A4B1 . . . . . B3 . B4 . . . B4 . . . A1A4B1B4 . . . B3 . B1 . . . . . . . B3 . A1A4B1B4 . B3 . B4 . B3 . B4 . . . B3 . . . A1A4B1B4 . . . B3 . B1 . . . . . . . . . A1A3B1 . . . . . . . . . B3 . B4 . B3 . A1A3B1B4 . . . B3 . B4 . . . . . B4 . B3 . A1A3A5B4 . B3 . B4 . B3 . B4 . . . B4 . B3 . A1A3A5B4 . . . B3 . B1 . . . . . B3 . . . A1A4B1 . . . . . . . . . . . B3 . . . A1A4B1B4 . . . B5 . B5 . . . . . . . . . A1A4B1B4 . B3 . B4 . B3 . B4 . B3 . B4 . . . A1A4B1B4 . . . B5 . B5 . . . . . . . . . A1A3B1 . . . B2 . . . B2 . . . B1 . . . A1A3B1B2 . . . B3 . . . B3 . . . . . . . A1A3A5 . . . C2 . . . B5 . . . B4 . . . A1A3A5B4 . . . . . B3 . B5 . . . . . . . A1A4B1B4 . . . . . . . . . . . . . . . A1A4B1B3 . B3 . . . B4 . . . . . . . . . A2A4B1 . . . C2 . . . C1 . . . . . . . A2A4B1 . . . B5 . . . B4 . . . . . . . A1A3B1 . . . B5 . . . B5 . . . . . . . A1A3B1 . . . B3 . . . B3 . . . . . . . A1A3A5 . . . B4 . . . B5 . . . . . . . A1A3A5 . . . B3 . . . B1 . . . . . . . A1A4B1 . . . B4 . . . B4 . . . . . . . A1A4B1B3 . B3 . . . B3 . . . . . . . . . A1A3A5B4 . B3 . B4 . . . B4 . B3 . B4 . B3 . A1A3A5B4 . B3 . B4 . B3 . . . . . B1 . . . A1A3B1 . . . . . . . . . . . B3 . . . A1A3B1 . . . . . . . . . . . B4 . . . A1A3A5B5 . . . B5 . . . B5 . . . B5 . . . A1A3A5B5 . . . . . . . B4 . . . . . . . A1A4B1B4 . . . B5 . . . B4 . . . B3 . . . B1 . . . . . . . C1 . . . . . . . A3B1B3B5 . . . . . . . . . . . . . . . B1 . . . . . . . C1 . . . . . . . A1A3B1B5 . . . . . . . . . . . . . . . . . . . . . . . . . . . B3 . . . A1A3A5B4 . . . . . . . . . . . B3 . . . B4 . . . . . . . B3 . . . . . . . A1A4B1B4 . . . B5 . . . B4 . . . B3 . . . B1 . . . . . . . C1 . . . . . . . A3B1B3B5 . . . . . . . . . . . . . . . B1 . . . . . . . C1 . . . . . . . A1A3B1B5 . . . . . . . . . . . B4 . . . . . . . . . . . . . . . B3 . . . A1A3A5B2 . . . . . . . B2 . . . B1 . . . B2 . . . B3 . . . . . . . . . . . A1A4B1B4 . . . B5 . . . B4 . . . B3 . . . B1 . . . . . . . C1 . . . . . . . A3B1B3B5 . . . . . . . . . . . . . . . B1 . . . . . . . C1 . . . . . . . A1A3B1B5 . . . . . . . . . . . . . . . . . . . . . . . . . . . B3 . . . A1A3A5B4 . . . . . . . . . . . B3 . . . B4 . . . . . . . B3 . . . . . . . A1A4B1B4 . . . B5 . . . B4 . . . B3 . . . B1 . . . . . . . C1 . . . . . . . A3B1B3B5 . . . . . . . . . . . . . . . B1 . . . . . . . C1 . . . . . . . A1A3B1B5 . . . . . . . . . . . B4 . . . . . . . . . . . . . . . B3 . . . A1A3A5B2 . . . . . . . B2 . . . B1 . . . B2 . . . B3 . . . . . . . . . . . A1A4B1B3 . . . . . . . . . . . B2 . . . B1 . . . . . . . . . . . A3 . . . A4 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . A2 . . . . . . . A4B1 . . . . . . . . . . . . . . . A4B1 . . . . . . . A1 . . . . . . . A3A5 . . . . . . . . . . . . . . . A3A5 . . . . . . . A1 . . . . . . . A2A5 . . . . . . . . . . . . . . . A2A5 . . . . . . . A1 . . . . . . . A2A5 . . . . . . . . . . . . . . . A2A5 . . . . . . . A2 . . . . . . . A4B1 . . . . . . . B5 . . . . . C1 . A4B1B5 . . . . . B5 . A1 . . . . . . . A3A5 . . . . . . . B5 . . . . . C1 . A3A5B5 . . . . . B5 . A2A5B2 . . . . . B4 . B2 . . . . . . . . . . . . . . . B3 . . . . . . . B2 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . A2 . . . . . . . A4B1 . . . . . . . B5 . . . . . C1 . A4B1B5 . . . . . B5 . A1 . . . . . . . A3A5 . . . . . . . B5 . . . . . C1 . A3A5B5 . . . . . B5 . A1 . . . . . B4 . A2A5B2 . . . . . . . . . . . . . . . A2A5B3 . . . . . . . A1B2 . . . . . . . A2A5 . . . . . B1 . A5 . . . . . . . A2 . . . . . . . A2 . . . . . . . A4B1 . . . . . . . B5 . . . . . C1 . A4B1B5 . . . . . B5 . A1 . . . . . . . A3A5 . . . . . . . B5 . . . . . C1 . A3A5B5 . . . . . B5 . A1 . . . . . B4 . A2A5B2 . . . . . . . . . . . . . . . A2A5 . . . . . . . A1 . . . . . . . A2A5 . . . B3 . . . B4 . . . . . . . A2A5B3 . . . . . . . A2A4B4 . . . B5 . . . A4B1B4 . . . B3 . . . B1 . . . . . . . A4B1C1 . . . . . . . A1B5 . . . . . . . A3A5 . . . . . . . B1 . . . . . . . A3A5C1 . . . . . . . A1A5B5 . . . . . . . A2A5 . . . . . . . . . . . . . . . A2A5 . . . B3 . . . A1A3B4 . . . . . . . A3A5 . . . B3 . . . B4 . . . . . . . A3A5B3 . . . . . . . A2A4B4 . . . B5 . . . A4B1B4 . . . B3 . . . B1 . . . . . . . A4B1C1 . . . . . . . A1B5 . . . . . . . A3A5 . . . . . . . B1 . . . . . . . A3A5C1 . . . . . . . A1A5B5 . . . . . . . A2A5 . . . B4 . . . . . . . . . . . A2A5 . . . B3 . . . A1A3B2 . . . . . . . A3A5B2 . . . B1 . . . B2 . . . B3 . . . A3A5 . . . . . . . A2A4B4 . . . B5 . . . A4B1B4 . . . B3 . . . B1 . . . . . . . A4B1C1 . . . . . . . A1B5 . . . . . . . A3A5 . . . . . . . B1 . . . . . . . A3A5C1 . . . . . . . A1A5B5 . . . . . . . A2A5 . . . . . . . . . . . . . . . A2A5 . . . B3 . . . A1A3B4 . . . . . . . A3A5 . . . B3 . . . B4 . . . . . . . A3A5B3 . . . . . . . A2A4B4 . . . B5 . . . A4B1B4 . . . B3 . . . B1 . . . . . . . A4B1C1 . . . . . . . A1B5 . . . . . . . A3A5 . . . . . . . B1 . . . . . . . A3A5C1 . . . . . . . A1A5B5 . . . . . . . A2A5 . . . B4 . . . . . . . . . . . A2A5 . . . B5 . . . A1A3B5 . . . . . . . A3A5B4 . . . B3 . . . B4 . . . B3 . . . A3A5 . . . . . . . A1A4B1 . . . . . . . . . . . B3 . . . B4 . . . . . B5 . . . . . B4 . . . A3B1B3 . . . . . . . . . . . . . . . B4 . . . . . B3 . . . . . B5 . . . A1A3B1 . . . . . . . . . . . B4 . . . B3 . . . . . . . . . . . B3 . . . A1A3A5B2 . . . . . . . B2 . . . B1 . . . B2 . . . B3 . . . . . . . . . . ."
    }
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
