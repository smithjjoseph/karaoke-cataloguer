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
from tkinter import ttk
from typing import Tuple
from pathlib import Path
from tkinter import messagebox
from numpy import column_stack

ctk.set_appearance_mode('system')
ctk.set_default_color_theme('blue')

WINDOW_SIZE: Tuple[int, int] = (640, 1000)
DATA_FILE: Path = Path(__file__, '..', 'data.csv').resolve()
HEADINGS: Tuple[str] = ('track_num', 'track_title', 'cd_num', 'cd_title')
HEAD_PROPS: Tuple[Tuple[str, int]] = (('Track No.', 80), ('Track Title', 240),
                                      ('CD No.', 80), ('CD Title', 240))


# TODO: Look into ttk styling for treeview
# https://docs.python.org/3/library/tkinter.ttk.html#ttk-styling


class App(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()
        self._window_setup()

        # Load data from CSV if exists
        if DATA_FILE.is_file():
            self.data = pd.read_csv('./data.csv', dtype=str)
        else:
            messagebox.showinfo("Error", message="No data file found",
                                icon="error", parent=None)
            exit(-1)


    def _window_setup(self) -> None:
        self.title('Karaoke CD Search')
        self.geometry(f"{WINDOW_SIZE[0]}x{WINDOW_SIZE[1]}")
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # TODO: Create a binding to link entry to _display_results()
        self.entry = ctk.CTkEntry(self)
        self.entry.grid(row=0, column=0, sticky='EW', padx=(10,10), pady=(10,10))
        # Setup tree view for output table
        self.output = ttk.Treeview(self, columns=tuple(HEADINGS))
        self.output['show'] = 'headings'
        for id, (heading, size) in zip(HEADINGS, HEAD_PROPS):
            self.output.column(id, width=size, anchor='center')
            self.output.heading(id, text=heading)

        self.output.grid(row=1, column=0, sticky='NESW', padx=(10,10), pady=(10,10))
        self.output.insert('', 'end', str(1))
        self.output.set(str(1), HEADINGS[0], '1')
        self.output.set(str(1), HEADINGS[1], 'Takin\' Care Of Business')
        self.output.set(str(1), HEADINGS[2], int('07'))
        self.output.set(str(1), HEADINGS[3], 'Sweet Georgia Brown SGB1001')


    def _get_results(self, search: str) -> pd.DataFrame:
        # Gets a list of bools for rows for which a regex match is found
        mask = column_stack(
            [self.data[col].str.contains(rf"(?:{search})", case=False, na=False) 
             for col in self.data])
        
        return self.data.loc[mask.any(axis=1)]


    def _display_results(self) -> None:
        # TODO: Replace with binding's contents
        search = 'all'

        self._get_results(search)
        # TODO: Display results using sample input above in _window_setup()


    def run(self):
        self.mainloop()


if __name__ == '__main__':
    pd.options.display.max_colwidth = 20

    app = App()
    app.run()

    print(app._get_results(search='all'))
