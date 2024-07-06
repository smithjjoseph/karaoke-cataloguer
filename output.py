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
from tkinter import Event, messagebox
from numpy import column_stack

ctk.set_appearance_mode('system')
ctk.set_default_color_theme('blue')

WINDOW_SIZE: Tuple[int, int] = (660, 1000)
DATA_FILE: Path = Path(__file__, '..', 'data.csv').resolve()
HEADINGS: Tuple[str] = ('track_num', 'track_title', 'cd_num', 'cd_title')
HEAD_PROPS: Tuple[Tuple[str, int]] = (('Track No.', 70), ('Track Title', 249),
                                      ('CD No.', 70), ('CD Title', 249))


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
        
        self._display_results(None)


    def _window_setup(self) -> None:
        self.title('Karaoke CD Search')
        self.geometry(f"{WINDOW_SIZE[0]}x{WINDOW_SIZE[1]}")
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.entry = ctk.CTkEntry(self)
        self.entry.grid(row=0, column=0, sticky='EW', padx=(10,10), pady=(10,10))
        # Create a binding to set _display_results() as a callback
        self.entry.bind('<KeyRelease>', self._display_results)
        # Setup tree view for output table
        self.output = ttk.Treeview(self, columns=tuple(HEADINGS))
        self.output['show'] = 'headings'
        for id, (heading, size) in zip(HEADINGS, HEAD_PROPS):
            self.output.column(id, width=size, anchor='center')
            self.output.heading(id, text=heading)
        self.output.grid(row=1, column=0, sticky='NESW', padx=(10,10), pady=(10,10))


    def _get_results(self, search: str) -> pd.DataFrame:
        # Gets a list of bools for rows for which a regex match is found
        mask = column_stack(
            [self.data[col].str.contains(rf"(?:{search})", case=False, na=False) 
             for col in self.data])
        
        return self.data.loc[mask.any(axis=1)]


    def _display_results(self, _: Event) -> None:
        # Get results based on entry
        search = self.entry.get()
        if search:
            res = self._get_results(search)
        else:
            res = self.data

        # Empty the treeview
        self.output.delete(*self.output.get_children())

        # Populate rows in treeview with found data
        for row in res.itertuples():
            self.output.insert('', 'end', row.Index)
            self.output.set(row.Index, HEADINGS[0], row.track_num)
            self.output.set(row.Index, HEADINGS[1], row.track_title)
            self.output.set(row.Index, HEADINGS[2], int(row.cd_num))
            self.output.set(row.Index, HEADINGS[3], row.cd_title)


    def run(self):
        self.mainloop()


if __name__ == '__main__':
    pd.options.display.max_colwidth = 20

    app = App()
    app.run()
