# import pyautogui
import pydirectinput
import time
import ctypes
import sys
from pick import pick
from src import song_parser, Song, songSheet, play_song
pydirectinput.PAUSE = 0.0


def _display_loader(n_secs: int = 2, fmt_str: str = "Starting in {n}s...", done_msg: str = "Playing song...") -> None:
    """
    Displays a loader for the user.

    :param n_secs: Number of seconds to display the loader
    :type n_secs: int
    :param fmt_str: Format string for the loader
    :type fmt_str: str
    :return: None
    """
    for i in range(n_secs, 0, -1):
        print(fmt_str.format(n=i), end="\r")
        time.sleep(1)
    print(done_msg.ljust(len(fmt_str.format(n=n_secs))))

def main():
    # Check if the user is an admin
    if not ctypes.windll.shell32.IsUserAnAdmin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        return

    option, index = pick(list(songSheet.keys()), "Select a song", indicator="->", default_index=0)
    _display_loader(n_secs=2, fmt_str="Starting in {n}s...", done_msg=f"Playing {songSheet[option].name}...")
    play_song(songSheet[option])


if __name__ == "__main__":
    main()