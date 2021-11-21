#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""データを読み込むモジュール"""
import csv

import numpy as np


def read_tracking(path: str) -> list:
    """トラッキングを読み込みリストにする

    Args:
        path (str): ファイルのパス

    Returns:
        list: トラッキングリスト
    """
    with open(path, "r") as f:
        lines = f.read().split('\n')
        tracking_list = [list(map(int, line.split(' ')))[:6] for line in lines]

    return tracking_list


def read_baseline(path: str) -> list:
    """[summary]

    Args:
        path (str): ファイルのパス

    Returns:
        list: 基準線の座標のリスト
    """
    with open(path, "r") as csvfile:
        reader = csv.reader(csvfile)
        baseline_list_csv = [row for row in reader]
        for i in range(1, len(baseline_list_csv)):
            baseline = np.reshape(
                np.array(baseline_list_csv[i], dtype=np.int32),[int(len(baseline_list_csv[i]) / 2), 2])

        return baseline