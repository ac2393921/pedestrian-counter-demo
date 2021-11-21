#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""歩行者情報を格納するモジュール"""

class Pedestrian:
    """歩行者クラス

    Attributes:
        tracking_id (int): トラッキングID
        start_point (tuple): エリアに入った座標
        start_time (float): エリアに入った時間
        point_frame (int): 指定の秒数ごとのフレーム
        position (tupple): 指定の秒数ごとの座標

        orbit_list (list): 軌道リスト
    """

    def __init__(self, tracking_id: int, start_point: tuple, frame_id: int, frame_rate: int, position: tuple) -> None:
        """[summary]

        Args:
            tracking_id (int): トラッキングID
            start_point (tuple): エリアに入った座標
            frame_id (int): フレームID
            frame_rate (int): フレームレート
            position (tuple): 指定の秒数ごとの座標
        """
        self.tracking_id = tracking_id
        self.start_point = start_point
        self.start_time = frame_id / frame_rate
        self.point_frame = frame_id
        self.position = position

        self.orbit_list = []

    def set_orbit(self, point: tuple) -> None:
        """軌道リストに軌道の座標を格納する

        Args:
            point (tuple): 軌道座標
        """
        self.orbit_list.append(point)

