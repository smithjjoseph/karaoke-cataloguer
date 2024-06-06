#!/usr/bin/python3
"""
:file: input.py
:brief: GUI with options for selecting area to use OCR on and text entry
        for editing any incorrect text
:author: Joseph Smith
"""

import re
import json
import csv
import pandas as pd
import customtkinter as ctk
from tkinter import messagebox
from ocr import OCR
from typing import List, Tuple
from pathlib import Path
from PIL import Image

IMAGE_PATH: Path = Path(__file__, '..', 'img').resolve()
IMAGE_FILES: List[str] = list(IMAGE_PATH.glob('*'))
WINDOW_SIZE: Tuple[int, int] = (1000, 640)
HEADINGS = ['track_num', 'track_title', 'cd_num', 'cd_title']

ctk.set_appearance_mode('system')
ctk.set_default_color_theme('blue')


class App(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()
        self._prepare_imgs()
        self._window_setup()

        self.ocr = OCR()
        self.data = pd.DataFrame(columns=HEADINGS)


    def _prepare_imgs(self):
        self.current_img = 0
        self.cd_imgs = []
        for img in IMAGE_FILES:
            img = ctk.CTkImage(Image.open(img), size=(400,400))
            self.cd_imgs.append(img)
        self.len_imgs = len(self.cd_imgs)


    def _window_setup(self):
        self.title('Karaoke CD Logger')
        self.geometry(f"{WINDOW_SIZE[0]}x{WINDOW_SIZE[1]}")
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Image frame
        self.frame_img = ctk.CTkFrame(self)
        self.frame_img.grid_rowconfigure(0, weight=1)
        self.frame_img.grid_columnconfigure(0, weight=1)
        self.frame_img.grid(row=0, column=0, padx=(20,10), pady=(20,10))
        self.lbl_CD = ctk.CTkLabel(self.frame_img, text=f"1/{self.len_imgs}", image=self.cd_imgs[0], compound="top", corner_radius=100)
        self.lbl_CD.grid(row=0, column=0, padx=(10,10), pady=(10,10))

        # Image Buttons Frame
        self.frame_btn = ctk.CTkFrame(self)
        self.frame_btn.grid_rowconfigure((0,1,2), weight=1)
        self.frame_btn.grid_columnconfigure((0,1), weight=1)
        self.frame_btn.grid(row=1, column=0, padx=(20,10), pady=(10,20), sticky='ew')
        self.btn_prev = ctk.CTkButton(self.frame_btn, text='Previous Image', command=self._prev_func)
        self.btn_prev.grid(row=0, column=0, sticky='ew', padx=(40,20), pady=(20,5))
        self.btn_next = ctk.CTkButton(self.frame_btn, text='Next Image', command=self._next_func)
        self.btn_next.grid(row=0, column=1, sticky='ew', padx=(20,40), pady=(20,5))
        self.btn_title = ctk.CTkButton(self.frame_btn, text='Select Title', command=self._title_func)
        self.btn_title.grid(row=1, column=0, sticky='ew', padx=(40,20), pady=(5,5))
        self.btn_tracks = ctk.CTkButton(self.frame_btn, text='Select Tracks', command=self._tracks_func)
        self.btn_tracks.grid(row=1, column=1, sticky='ew', padx=(20,40), pady=(5,5))
        self.btn_submit = ctk.CTkButton(self.frame_btn, text='Submit to DB', command=self._submit_func)
        self.btn_submit.grid(row=2, column=0, columnspan=2, padx=(10,10), pady=(5,20))

        # Textboxes
        self.txt_tracks = ctk.CTkTextbox(self, width=200, font=(None,20))
        self.txt_tracks.grid(row=0, column=1, padx=(10,20), pady=(20,10), sticky="nsew")
        self.txt_title = ctk.CTkTextbox(self, width=200, font=(None,20))
        self.txt_title.grid(row=1, column=1, padx=(10,20), pady=(10,20), sticky="nsew")


    def run(self):
        self.mainloop()


    def _get_tb(self, tb: ctk.CTkTextbox):
        txt = tb.get('1.0', 'end-1c')
        return None if txt == '' else txt


    def _warn(self, msg):
        messagebox.showinfo("Error", msg, icon="warning", parent=None)


    def _remember(self) -> None:
        title = self._get_tb(self.txt_title).strip()
        tracks = self._get_tb(self.txt_tracks)
        if not title or not tracks:
            self._warn("Missing either track list or title.")
            return
        tracks = list(filter(None, tracks.split('\n')))

        # Repeated insertion to a df is inefficient, O(n^2)
        # Append using list instead, O(n), then concatenate
        extension = []
        for line in tracks:
            num, sep, track = line.partition('.')

            if not sep:
                self._warn("Track list is not properly formatted.")
                return

            extension.append([num.strip(), track.strip(), 
                              self.current_img, title])

        addition = pd.DataFrame(extension, columns=HEADINGS)

        # If duplicate track_num & cd_num entires exist, delete old values
        self.data = self.data.drop(
            self.data[self.data.cd_num == self.current_img].index)

        self.data = pd.concat([self.data, addition])
        self.data = self.data.reset_index(drop=True)


    def _recall(self) -> None:
        # TODO:
        # Check if there is data for this image
        # Load the data if possible
        raise NotImplementedError()


    def _prev_func(self) -> None:
        if self.current_img <= 0:
            return
        self.current_img -= 1
        self.lbl_CD.configure(text=f"{self.current_img+1}/{self.len_imgs}")
        self.lbl_CD.configure(image=self.cd_imgs[self.current_img])
        # Call _remember
        # Call _clear
        # Call _recall


    def _next_func(self) -> None:
        if self.current_img >= self.len_imgs-1:
            return
        self.current_img += 1
        self.lbl_CD.configure(text=f"{self.current_img+1}/{self.len_imgs}")
        self.lbl_CD.configure(image=self.cd_imgs[self.current_img])
        # Call _remember
        # Call _clear
        # Call _recall


    def _title_func(self) -> None:
        title = self.ocr.identify(str(IMAGE_FILES[self.current_img]))
        self.txt_title.delete(1.0, ctk.END)
        self.txt_title.insert(1.0, ' '.join(title))


    def _tracks_func(self) -> None:
        tracks = self.ocr.identify(str(IMAGE_FILES[self.current_img]))

        # There are definitely issues with the logic here but who cares
        tracks = ' '.join(tracks)
        tracks = re.sub('(?<= )(\d+[\.:])', '\n\g<0>', tracks)
        track_list = [track.strip() for track in tracks.splitlines()]

        self.txt_tracks.delete(1.0, ctk.END)
        for i, track in enumerate(track_list):
            self.txt_tracks.insert(f"{i+1}.0", track + '\n')


    def _submit_func(self) -> None:
        # Add current CD to df
        self._remember()
        # Convert DataFrame to csv/json and save
        # raise NotImplementedError()


if __name__ == '__main__':
    pd.options.display.max_colwidth = 20

    app = App()
    app.run()
