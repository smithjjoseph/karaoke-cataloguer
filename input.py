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
IMAGE_FILES: List[Path] = list(IMAGE_PATH.glob('*'))
DISC_NUMS: List[str] = [str(file.name)[:-4] for file in IMAGE_FILES]
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


    def _prepare_imgs(self) -> None:
        self.current_img = 0
        self.cd_imgs = []
        for img in IMAGE_FILES:
            img = ctk.CTkImage(Image.open(img), size=(400,400))
            self.cd_imgs.append(img)
        self.len_imgs = len(self.cd_imgs)


    def _window_setup(self) -> None:
        self.title('Karaoke CD Logger')
        self.geometry(f"{WINDOW_SIZE[0]}x{WINDOW_SIZE[1]}")
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Image frame
        self.frame_img = ctk.CTkFrame(self)
        self.frame_img.grid_rowconfigure(0, weight=1)
        self.frame_img.grid_columnconfigure(0, weight=1)
        self.frame_img.grid(row=0, column=0, padx=(20,10), pady=(20,10))
        self.lbl_CD = ctk.CTkLabel(self.frame_img, 
                                   text=f"Disc {DISC_NUMS[self.current_img]}\t"
                                        f"1/{self.len_imgs}", 
                                   image=self.cd_imgs[0], 
                                   compound="top", 
                                   corner_radius=100)
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


    def run(self) -> None:
        self.mainloop()


    def _get_tb(self, tb: ctk.CTkTextbox) -> str | None:
        txt = tb.get('1.0', 'end-1c')
        return txt or None


    def _warn(self, msg):
        messagebox.showinfo("Error", msg, icon="warning", parent=None)


    def _remember(self) -> bool:
        """Stores current text box contents in dataframe

        :return: Whether or not there was a failure saving contents
                 False if there was an actionable failure
                 True if there was not an actionable failure
        :rtype: bool
        """
        title = self._get_tb(self.txt_title)
        tracks = self._get_tb(self.txt_tracks)
        if not title or not tracks:
            # Assumes the user is skipping past the CD
            return True
        title = title.strip()
        tracks = list(filter(None, tracks.split('\n')))
        cd_num = DISC_NUMS[self.current_img]

        # Repeated insertion to a df is inefficient, O(n^2)
        # Append using list instead, O(n), then concatenate
        extension = []
        for line in tracks:
            num, sep, track = line.partition('.')

            if not sep:
                self._warn("Track list is not properly formatted.")
                return False

            extension.append([num.strip(), track.strip(),
                              cd_num, title])

        addition = pd.DataFrame(extension, columns=HEADINGS)

        # If duplicate track_num & cd_num entires exist, delete old values
        self.data = self.data.drop(
            self.data[self.data.cd_num == cd_num].index)

        self.data = pd.concat([self.data, addition])
        self.data = self.data.reset_index(drop=True)

        return True


    def _clear(self) -> None:
        self.txt_title.delete('1.0', ctk.END)
        self.txt_tracks.delete('1.0', ctk.END)


    def _recall(self) -> None:
        cd_num = DISC_NUMS[self.current_img]
        # Pandas queries for CD title and track information
        query = self.data[self.data["cd_num"] == cd_num]
        title = query['cd_title']
        track_query = query[['track_num', 'track_title']]

        # Return if there is no track listing for current CD
        if title.empty or track_query.empty:
            return

        title = title.values[0]
        track_list = track_query.values
        tracks = ''
        # Format track information in string
        for num, track in track_list:
            tracks += f"{num}.{track}\n"

        # Put formatted data into entries
        self.txt_title.insert(ctk.END, title)
        self.txt_tracks.insert(ctk.END, tracks)


    def _prev_func(self) -> None:
        if self.current_img <= 0:
            return

        if not self._remember():
            return
        self._clear()

        self.current_img -= 1
        self._recall()
        self.lbl_CD.configure(text=f"Disc {DISC_NUMS[self.current_img]}\t"
                                   f"{self.current_img+1}/{self.len_imgs}")
        self.lbl_CD.configure(image=self.cd_imgs[self.current_img])


    def _next_func(self) -> None:
        if self.current_img >= self.len_imgs-1:
            return

        if not self._remember():
            return
        self._clear()

        self.current_img += 1
        self._recall()
        self.lbl_CD.configure(text=f"Disc {DISC_NUMS[self.current_img]}\t"
                                   f"{self.current_img+1}/{self.len_imgs}")
        self.lbl_CD.configure(image=self.cd_imgs[self.current_img])


    def _title_func(self) -> None:
        title = self.ocr.identify(str(IMAGE_FILES[self.current_img]))
        if not title:
            return

        # Replace any old title text with the new text from OCR
        self.txt_title.delete(1.0, ctk.END)
        self.txt_title.insert(1.0, ' '.join(title))


    def _tracks_func(self) -> None:
        tracks = self.ocr.identify(str(IMAGE_FILES[self.current_img]))
        if not tracks:
            return

        # Attempt to pretty parse text from OCR
        # There are definitely issues with the logic here but who cares
        tracks = ' '.join(tracks)
        tracks = re.sub('(?<= )(\d+[\.:])', '\n\g<0>', tracks)
        track_list = [track.strip() for track in tracks.splitlines()]

        # Replace any old track text with the new text from OCR
        self.txt_tracks.delete(1.0, ctk.END)
        for i, track in enumerate(track_list):
            self.txt_tracks.insert(f"{i+1}.0", track + '\n')


    def _submit_func(self) -> None:
        # Ensure current CD is added to df
        if not self._remember():
            return
        # TODO: Convert DataFrame to csv/json and save for use in output.py
        raise NotImplementedError()


if __name__ == '__main__':
    pd.options.display.max_colwidth = 20

    app = App()
    app.run()
