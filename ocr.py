#!/usr/bin/python3
"""
:file: ocr.py
:brief: OCR helper commands for use with input GUI app
:author: Joseph Smith
"""

import cv2
import numpy as np
from typing import List
from paddleocr import PaddleOCR
from screeninfo import get_monitors


class OCR:
    def __init__(self, init_ocr:bool=True) -> None:
        # OCR can be disabled for debug since it has a long load time
        if not init_ocr:
            return

        # See '6 Parameter Description' @ https://pypi.org/project/paddleocr/
        # for full list of parameters
        # Ran only once to download and load appropriate model into memory
        self.ocr = PaddleOCR(lang="en", show_log=False)


    @staticmethod
    def crop(img_path: str) -> np.ndarray:
        raw_img = cv2.imread(img_path)

        # Image might need to be resized otherwise it doesn't fully display
        img_height, *_ = raw_img.shape
        monitor_height = [m.height for m in get_monitors() if m.is_primary][0]
        ratio = 1
        if img_height > monitor_height:
            ratio = monitor_height/img_height - 0.05
        mini_img = cv2.resize(raw_img, None, fx=ratio, fy=ratio)

        roi = cv2.selectROI(mini_img)
        roi_crop = mini_img[int(roi[1]):int(roi[1]+roi[3]),
                           int(roi[0]):int(roi[0]+roi[2])]
        cv2.destroyAllWindows()

        return roi_crop


    def recognise(self, img: np.ndarray) -> List[str]:
        result = self.ocr.ocr(img, det=True, cls=False)
        text = [text[1][0] for text in [line for line in result[0]]]

        return text


    def identify(self, img_path: str) -> List[str]:
        roi = self.crop(img_path)
        text = self.recognise(roi)

        return text


if __name__ == '__main__':
    IMG_PATH: str = './img/karaoke.jpg'

    ocr: OCR = OCR()
    text: List[str] = ocr.identify(IMG_PATH)
    print('\n' + '\n'.join(text))
