#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""動画をキャプチャするモジュール"""
import os

import cv2


def capture():
    """動画をキャプチャする
    """
    cap = cv2.VideoCapture('../../data/video/demo.mp4')
    DIR_PATH = '../../data/image'

    if not os.path.exists(DIR_PATH):
        os.makedirs(DIR_PATH)

    save_press_count = 1
    while True:
        presskey = cv2.waitKey(1)

        if not cap.isOpened():
            break

        ret, frame = cap.read()

        if ret:
            cv2.imwrite(f"{DIR_PATH}/capture_{save_press_count}.png", frame)
            save_press_count += 1

            break
        else:
            break

    cap.release()

if __name__ == '__main__':
    capture()