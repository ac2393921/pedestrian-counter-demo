#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""歩行者をカウントし描画するモジュール"""

import threading

import cv2
import numpy as np
import pandas as pd
from pandas.core.frame import DataFrame

from utils import Pedestrian


class PedestrianCounter:
    """歩行者をカウントする

    Attributes:
        tracking_list (list): トラッキングリスト
        baseline (list): 基準線
        input_video (VideoCapture): インプット動画
        frame_size (tuple): フレームサイズ
        frame_rate (int): フレームレート
        frame_count (int): フレーム数
        output_video (VideoCapture): アウトプット動画
        centerline_left (tuple): 基準線の左座標
        centerline_right (tuple): 基準線の右座標
        center_vector (ndarray): 基準線のベクトル
        up_cnt (int): 上へ移動した歩行者のカウント数
        down_cnt (int): 下へ移動した歩行者のカウント数
        frame_id (int): フレームID
        pedestrian_list (list): 歩行者リスト
        ALPHA (float): アルファ値
    """

    ALPHA = 0.2

    def __init__(self, tracking_list: list, baseline: list, input_video_path: str, output_video_path: str) -> None:
        """init

        Args:
            tracking_list (list): トラッキングリスト
            baseline (list): 基準線
            input_video_path (str): インプット動画のパス
            output_video_path (str): アウトプット動画のパス
        """
        self.tracking_list = tracking_list
        self.baseline = baseline
        self.input_video = cv2.VideoCapture(input_video_path)
        self.frame_size = int(self.input_video.get(cv2.CAP_PROP_FRAME_WIDTH)), int(self.input_video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.frame_rate = int(self.input_video.get(cv2.CAP_PROP_FPS))
        self.frame_count = int(self.input_video.get(cv2.CAP_PROP_FRAME_COUNT))
        self.output_video = cv2.VideoWriter(output_video_path, cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), self.frame_rate, self.frame_size)
        self.centerline_left = (self.baseline[0][0], (self.baseline[0][1]+baseline[3][1])//2)
        self.centerline_right = (self.baseline[1][0], (self.baseline[1][1]+baseline[2][1])//2)
        self.center_vector = np.array(self.centerline_right)-np.array(self.centerline_left)   

        self.up_cnt = 0
        self.down_cnt = 0
        self.frame_id = 0
        self.pedestrian_list = []

    def draw(self) -> None:
        """歩行者カウントを描画する"""
        df = pd.DataFrame(self.tracking_list, columns=['frame_id', 'tracking_id', 'x', 'y', 'w', 'h'])
        df['center_x'] = df['x'] + df['w'] / 2

        while True:
            ret, frame = self.input_video.read()

            if ret:
                layer = frame.copy()

                current_frame = df.loc[df['frame_id'] == self.frame_id, ['frame_id', 'tracking_id', 'x', 'y', 'w', 'h', 'center_x']]

                for tracking_id in current_frame['tracking_id'].unique():
                    current = current_frame.loc[current_frame['tracking_id'] == tracking_id]
                    point = (int(current.center_x), int(current.y+current.h))

                    new = True

                    if (cv2.pointPolygonTest(self.baseline, point, False) == 1):
                        v = np.array(point)-np.array(self.centerline_left)
                        outer = np.cross(self.center_vector, v)

                        for pedestrian in self.pedestrian_list:
                            if pedestrian.tracking_id == tracking_id:
                                new = False

                                if self.frame_id - pedestrian.point_frame > 5:
                                    pedestrian.set_orbit(point)
                                    pedestrian.point_frame = self.frame_id

                                th_plot_orbit = threading.Thread(target=self.plot_orbit(frame, pedestrian))
                                th_plot_orbit.start()

                        if new:
                            if outer < 0:
                                position = 'up'
                            else:
                                position = 'down'

                            p = Pedestrian(tracking_id, point, self.frame_id, self.frame_rate, position)
                            self.pedestrian_list.append(p)

                    for pedestrian in self.pedestrian_list:
                        if pedestrian.tracking_id == tracking_id:
                            if (cv2.pointPolygonTest(self.baseline, point, False) <= 0):
                                v = np.array(point)-np.array(self.centerline_left)
                                outer = np.cross(self.center_vector, v)

                                if outer < 0 and pedestrian.position == 'down':
                                    self.down_cnt += 1
                                elif outer >= 0 and pedestrian.position == 'up':
                                    self.up_cnt += 1

                                self.pedestrian_list.pop(self.pedestrian_list.index(pedestrian))
                                break

                th_plot_bbox = threading.Thread(target=self.plot_bbox(frame, current_frame))
                th_plot_bbox.start()

                layer = cv2.fillConvexPoly(layer, self.baseline, (255, 0, 0))
                cv2.line(frame, self.centerline_left, self.centerline_right, (0, 0, 255), thickness=2, lineType=cv2.LINE_8)
                
                frame = cv2.addWeighted(frame, 1-self.ALPHA, layer, self.ALPHA, 0)

                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(frame, f'Up: {self.up_cnt}', (0,100), font, 4, (0,0,255), 2, cv2.LINE_AA)
                cv2.putText(frame, f'Down: {self.down_cnt}', (0,200), font, 4, (255,0,0), 2, cv2.LINE_AA)

                self.output_video.write(frame)

                print(f"{str(self.frame_id)}/{str(self.frame_count)}")

                self.frame_id += 1
            else:
                break

    def plot_bbox(self, frame: np.ndarray, tracking_df: DataFrame) -> None:
        """Bboxを描画する

        Args:
            frame (np.ndarray): フレーム
            tracking_df (DataFrame): フレームのトラッキングデータ
        """
        for tracking in tracking_df.itertuples():
            cv2.rectangle(frame, (tracking.x, tracking.y), (tracking.x+tracking.w, tracking.y+tracking.h), (0, 255, 0), 2)

    def plot_orbit(self, frame: np.ndarray, pedestrian: Pedestrian) -> None:
        """歩行者の軌道を描画する

        Args:
            frame (np.ndarray): フレーム
            pedestrian (Pedestrian): 歩行者
        """
        for orbit_point in pedestrian.orbit_list:
            if pedestrian.position == 'down':
                cv2.circle(frame, center=orbit_point, radius=3, color=(128, 128, 255), thickness=-1)
            else:
                cv2.circle(frame, center=orbit_point, radius=3, color=(255, 128, 128), thickness=-1)

    def close_video(self) -> None:
        """動画をリリースする"""
        self.input_video.release()
        self.output_video.release()
