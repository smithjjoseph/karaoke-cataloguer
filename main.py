#!/usr/bin/python3
"""
:file: main.py
:brief: CLI entry point for the input/output apps for the Karaoke project
:author: Joseph Smith
"""

import customtkinter as ctk
from typing import Tuple

WINDOW_SIZE: Tuple[int, int] = (600, 300)

ctk.set_appearance_mode('system')
ctk.set_default_color_theme('blue')


class App(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()
        self._window_setup()


    def _window_setup(self):
        self.title('Karaoke CD Logger')
        self.geometry(f"{WINDOW_SIZE[0]}x{WINDOW_SIZE[1]}")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure((0,1), weight=1)

        btn_font = ctk.CTkFont(family=None, size=36, weight='bold')
        self.input = ctk.CTkButton(self, text='INPUT', font=btn_font,
                                   command=self._input_app)
        self.input.grid(row=0, column=0, sticky='NESW', padx=(10,10),
                        pady=(10,10))
        self.output = ctk.CTkButton(self, text='OUTPUT', font=btn_font,
                                    command=self._output_app)
        self.output.grid(row=0, column=1, sticky='NESW', padx=(10,10),
                         pady=(10,10))


    def _input_app(self):
        import input
        mode = input.App(parent=self)
        mode.run()


    def _output_app(self):
        import output
        mode = output.App(parent=self)
        mode.run()


if __name__ == '__main__':
    app = App()
    app.mainloop()
