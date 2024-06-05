#!/usr/bin/python3
"""
:file: output.py
:brief: GUI with functionality for autocomplete search of tracks in a CSV
        returning completed track title as well as track number, CD number,
        and CD title
:author: Joseph Smith
"""

import pandas as pd
import customtkinter as ctk
from typing import Tuple

ctk.set_appearance_mode('system')
ctk.set_default_color_theme('blue')

WINDOW_SIZE: Tuple[int, int] = (1000, 640)


class App(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()
        self._window_setup()


    def _window_setup(self):
        self.title('Karaoke CD Search')
        self.geometry(f"{WINDOW_SIZE[0]}x{WINDOW_SIZE[1]}")

        # Import data from CSV into DataFrame
        # Entry and textbox
        # Everytime text is input in the entry the textbox will update to
        #  give all possible autocompletions to the desired song


    def run(self):
        self.mainloop()


if __name__ == '__main__':
    app = App()
    app.run()
