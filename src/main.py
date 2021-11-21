#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time


from utils import PedestrianCounter, read_tracking, read_baseline


DATA_PATH = '../data/'


def main():
    start_time = time.time()

    tracking_list = read_tracking(f'{DATA_PATH}tracking/demo.txt')
    baseline = read_baseline(f'{DATA_PATH}csv/baseline.csv')

    pc = PedestrianCounter(
        tracking_list,
        baseline,
        f'{DATA_PATH}video/demo.mp4',
        f'{DATA_PATH}output/output.mp4')

    pc.draw()
    pc.close_video()

    end_time = time.time()
    print("time is ", end_time - start_time, "'s")


if __name__ == "__main__":
    main()
