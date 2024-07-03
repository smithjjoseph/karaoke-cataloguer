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


    def _resize(img_path: str) -> np.ndarray:
        raw_img = cv2.imread(img_path)

        # Image might need to be resized otherwise it doesn't fully display
        img_height, *_ = raw_img.shape
        monitor_height = [m.height for m in get_monitors() if m.is_primary][0]
        if img_height > monitor_height:
            ratio = monitor_height/img_height - 0.05
        else:
            ratio = 1
        return cv2.resize(raw_img, None, fx=ratio, fy=ratio)


    @staticmethod
    def crop(img_path: str) -> np.ndarray:
        mini_img = OCR._resize(img_path)

        roi = cv2.selectROI(mini_img)
        roi_crop = mini_img[int(roi[1]):int(roi[1]+roi[3]),
                           int(roi[0]):int(roi[0]+roi[2])]
        cv2.destroyAllWindows()

        return roi_crop
    

    @staticmethod
    def display(img_path: str) -> None:
        mini_img = OCR._resize(img_path)

        cv2.imshow('Image Preview', mini_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


    def recognise(self, img: np.ndarray) -> List[str]:
        result = self.ocr.ocr(img, det=True, cls=False)
        if result[0] is None:
            return None
        else:
            return [text[1][0] for text in [line for line in result[0]]]



    def identify(self, img_path: str) -> List[str]:
        roi = self.crop(img_path)
        # Handle None return from OCR
        if text := self.recognise(roi):
            return text
        else:
            return None


if __name__ == '__main__':
    IMG_PATH: str = './img/10.jpg'

    ocr: OCR = OCR()
    text: List[str] = ocr.identify(IMG_PATH)
    if text:
        print('OCR example output:')
        print('\n' + '\n'.join(text))
