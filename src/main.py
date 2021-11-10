import sys

import cv2
import pandas as pd


def main():
    input_vide = cv2.VideoCapture('../data/video/demo.mp4')

    if not input_vide.isOpened():
        sys.exit()

    frame_size = int(input_vide.get(cv2.CAP_PROP_FRAME_WIDTH)), int(input_vide.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_rate = int(input_vide.get(cv2.CAP_PROP_FPS))
    frame_count = int(input_vide.get(cv2.CAP_PROP_FRAME_COUNT))

    with open('../data/tracking/demo.txt', "r") as f:
        lines = f.read().split('\n')
        tracking_list = [list(map(int, line.split(' ')))[:6] for line in lines]

    df = pd.DataFrame(tracking_list, columns=['frame_id', 'tracking_id', 'x', 'y', 'w', 'h'])
    df['center_x'] = df['x'] + df['w'] / 2

    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    output_video = cv2.VideoWriter('../data/output/output.mp4', fourcc, frame_rate, frame_size)

    frame_id = 1

    while True:
        ret, frame = input_vide.read()

        if ret:
            current_frame = df.loc[df['frame_id'] == frame_id, ['frame_id', 'tracking_id', 'x', 'y', 'w', 'h', 'center_x']]

            for c in current_frame.itertuples():
                cv2.rectangle(frame, (c.x, c.y), (c.x+c.w, c.y+c.h), (0, 255, 0), 2)
                cv2.circle(frame, center=(int(c.center_x), int(c.y+c.h)), radius=10,
                            color=(0, 0, 255), thickness=-1, lineType=cv2.cv2.LINE_4)

            output_video.write(frame)

            print(f"{str(frame_id)}/{str(frame_count)}")

            frame_id += 1
        else:
            break   

    input_vide.release()
    output_video.release()


if __name__ == "__main__":
    main()