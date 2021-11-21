#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""画像をクリックした箇所の座標を取得するモジュール"""

import numpy as np
import cv2


#データ点数
data_num = 9

#データ点格納用
points = np.zeros([2,data_num,2],dtype = int) #格納配列
pt = np.array([0,0]) #要素地点管理

#マウスイベント処理(leftimg)
def mouse_event_l(event, x, y, flags, param):
    #配列外参照回避
    if pt[0] > (data_num-1):
        return
    #クリック地点を配列に格納
    if event == cv2.EVENT_LBUTTONUP:
        points[0][pt[0]] = [x,y] #格納
        cv2.circle(window_l, (x,y), 5, (255,0,0), -1)
        pt[0] += 1 #要素地点を1つ増やす
        print(points)

#画像の読み込み
window_l = cv2.imread("../../data/image/capture_1.png", 1) #leftimg

#ウィンドウ生成
cv2.namedWindow("window_l", cv2.WINDOW_KEEPRATIO) #leftimg

#マウスイベント時に関数mouse_eventの処理を行う
cv2.setMouseCallback("window_l", mouse_event_l) #leftimg

#「q」が押されるまでループ
while True:
    #画像の表示
    cv2.imshow("window_l", window_l) #leftimg

    #キー入力
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cv2.destroyAllWindows()