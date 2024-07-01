import os
import cv2
import numpy as np
import sys
import time
from time import sleep
from dotenv import load_dotenv
from picamera2 import Picamera2

# Load configuration from .env file
load_dotenv()
IMAGE_SAVE_PATH = os.getenv("IMAGE_SAVE_PATH")
CAMERA_RESOLUTION_WIDTH = int(os.getenv("CAMERA_RESOLUTION_WIDTH"))
CAMERA_RESOLUTION_HEIGHT = int(os.getenv("CAMERA_RESOLUTION_HEIGHT"))
PREVIEW_WIDTH = int(os.getenv("PREVIEW_WIDTH"))
PREVIEW_HEIGHT = int(os.getenv("PREVIEW_HEIGHT"))

font = cv2.FONT_HERSHEY_SIMPLEX
fontScale = 0.7
color = (255, 255, 255)
thickness = 2

os.environ["DISPLAY"] = ':0.0'
window_name = "Focus"

cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (PREVIEW_WIDTH, PREVIEW_HEIGHT)}))
picam2.start()

width = 1280
height = 1024

org1 = (20, 30)
org2 = (int(width / 4 * 3) - 30, 30)
org3 = (20, int(height) - 20)
org4 = (int(width / 4 * 3) - 30, int(height) - 20)
orgmid = (int(width / 4) + 20, int(height / 4 * 3) + 20)

count = 0
count1 = 0
count2 = 0
count3 = 0
count4 = 0
countmid = 0

calibration = True
focus = False
focustol = 0.005  # Abweichung in Prozent (grün)
focustol2 = 0.08  # Abweichung in Prozent (gelb)

while True:
    keys = cv2.waitKey(1)
    count += 1
    frame = picam2.capture_array()
    frame = frame[:, :, 0:3]
    frame = cv2.rotate(frame, cv2.ROTATE_180)
    grayframe = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cleanframe = frame
    grayframe = cv2.GaussianBlur(grayframe, (3, 3), 0)
    edges = cv2.Canny(grayframe, 100, 100)
    frame = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

    upper_left = edges[0:int(height / 4), 0:int(width / 4)]
    upper_right = edges[0:int(height / 4), int(width * 0.75):int(width)]
    lower_left = edges[int(height * 0.75):int(height), 0:int(width / 4)]
    lower_right = edges[int(height * 0.75):int(height), int(width * 0.75):int(width)]
    mid = edges[int(height / 4):int(height * 3 / 4), int(width / 4):int(width * 3 / 4)]

    white_pixels1 = np.sum(upper_left == 255)
    white_pixels2 = np.sum(upper_right == 255)
    white_pixels3 = np.sum(lower_left == 255)
    white_pixels4 = np.sum(lower_right == 255)
    white_pixelsmid = np.sum(mid == 255)

    if calibration:
        if white_pixels1 > tmp1:
            tmp1 = white_pixels1
            count1 = count
        if white_pixels2 > tmp2:
            tmp2 = white_pixels2
            count2 = count
        if white_pixels3 > tmp3:
            tmp3 = white_pixels3
            count3 = count
        if white_pixels4 > tmp4:
            tmp4 = white_pixels4
            count4 = count
        if white_pixelsmid > tmpmid:
            tmpmid = white_pixelsmid
            countmid = count

    lineth = 4
    if focus:
        def draw_focus_rect(condition, rect_coords, color):
            if condition:
                cv2.rectangle(frame, rect_coords[0], rect_coords[1], color, lineth)

        draw_focus_rect(white_pixels1 > tmp1 - int(white_pixels1 * focustol),
                        ((0 + int(lineth / 4), 0 + int(lineth / 4)), (int(width / 4) - int(lineth / 4), int(height / 4) - int(lineth / 4))),
                        (0, 255, 0))
        draw_focus_rect((white_pixels1 < tmp1 - int(white_pixels1 * focustol)) and (white_pixels1 > tmp1 - int(white_pixels1 * focustol2)),
                        ((0 + int(lineth / 4), 0 + int(lineth / 4)), (int(width / 4) - int(lineth / 4), int(height / 4) - int(lineth / 4))),
                        (0, 255, 255))
        draw_focus_rect(white_pixels1 < tmp1 - int(white_pixels1 * focustol2),
                        ((0 + int(lineth / 4), 0 + int(lineth / 4)), (int(width / 4) - int(lineth / 4), int(height / 4) - int(lineth / 4))),
                        (0, 0, 255))

        draw_focus_rect(white_pixels2 > tmp2 - int(white_pixels2 * focustol),
                        ((int(width / 4 * 3) + int(lineth / 4), 0 + int(lineth / 4)), (int(width) - int(lineth / 4), int(height / 4) - int(lineth / 4))),
                        (0, 255, 0))
        draw_focus_rect((white_pixels2 < tmp2 - int(white_pixels2 * focustol)) and (white_pixels2 > tmp2 - int(white_pixels2 * focustol2)),
                        ((int(width / 4 * 3) + int(lineth / 4), 0 + int(lineth / 4)), (int(width) - int(lineth / 4), int(height / 4) - int(lineth / 4))),
                        (0, 255, 255))
        draw_focus_rect(white_pixels2 < tmp2 - int(white_pixels2 * focustol2),
                        ((int(width / 4 * 3) + int(lineth / 4), 0 + int(lineth / 4)), (int(width) - int(lineth / 4), int(height / 4) - int(lineth / 4))),
                        (0, 0, 255))

        draw_focus_rect(white_pixels3 > tmp3 - int(white_pixels3 * focustol),
                        ((0 + int(lineth / 4), int(height / 4 * 3) + int(lineth / 4)), (int(width / 4) - int(lineth / 4), int(height) - int(lineth / 4))),
                        (0, 255, 0))
        draw_focus_rect((white_pixels3 < tmp3 - int(white_pixels3 * focustol)) and (white_pixels3 > tmp3 - int(white_pixels3 * focustol2)),
                        ((0 + int(lineth / 4), int(height / 4 * 3) + int(lineth / 4)), (int(width / 4) - int(lineth / 4), int(height) - int(lineth / 4))),
                        (0, 255, 255))
        draw_focus_rect(white_pixels3 < tmp3 - int(white_pixels3 * focustol2),
                        ((0 + int(lineth / 4), int(height / 4 * 3) + int(lineth / 4)), (int(width / 4) - int(lineth / 4), int(height) - int(lineth / 4))),
                        (0, 0, 255))

        draw_focus_rect(white_pixels4 > tmp4 - int(white_pixels4 * focustol),
                        ((int(width / 4 * 3) + int(lineth / 4), int(height / 4 * 3) + int(lineth / 4)), (int(width) - int(lineth / 4), int(height) - int(lineth / 4))),
                        (0, 255, 0))
        draw_focus_rect((white_pixels4 < tmp4 - int(white_pixels4 * focustol)) and (white_pixels4 > tmp4 - int(white_pixels4 * focustol2)),
                        ((int(width / 4 * 3) + int(lineth / 4), int(height / 4 * 3) + int(lineth / 4)), (int(width) - int(lineth / 4), int(height) - int(lineth / 4))),
                        (0, 255, 255))
        draw_focus_rect(white_pixels4 < tmp4 - int(white_pixels4 * focustol2),
                        ((int(width / 4 * 3) + int(lineth / 4), int(height / 4 * 3) + int(lineth / 4)), (int(width) - int(lineth / 4), int(height) - int(lineth / 4))),
                        (0, 0, 255))

        draw_focus_rect(white_pixelsmid > tmpmid - int(white_pixelsmid * focustol),
                        ((int(width / 4) + int(lineth / 4), int(height / 4) + int(lineth / 4)), (int(width * 3 / 4) - int(lineth / 4), int(height * 3 / 4) - int(lineth / 4))),
                        (0, 255, 0))
        draw_focus_rect((white_pixelsmid < tmpmid - int(white_pixelsmid * focustol)) and (white_pixelsmid > tmpmid - int(white_pixelsmid * focustol2)),
                        ((int(width / 4) + int(lineth / 4), int(height / 4) + int(lineth / 4)), (int(width * 3 / 4) - int(lineth / 4), int(height * 3 / 4) - int(lineth / 4))),
                        (0, 255, 255))
        draw_focus_rect(white_pixelsmid < tmpmid - int(white_pixelsmid * focustol2),
                        ((int(width / 4) + int(lineth / 4), int(height / 4) + int(lineth / 4)), (int(width * 3 / 4) - int(lineth / 4), int(height * 3 / 4) - int(lineth / 4))),
                        (0, 0, 255))

    cv2.putText(frame, f"{white_pixels1}    Max: {tmp1} Time: {count1}", org1, font, fontScale, color, thickness)
    cv2.putText(frame, f"{white_pixels2}    Max: {tmp2} Time: {count2}", org2, font, fontScale, color, thickness)
    cv2.putText(frame, f"{white_pixels3}    Max: {tmp3} Time: {count3}", org3, font, fontScale, color, thickness)
    cv2.putText(frame, f"{white_pixels4}    Max: {tmp4} Time: {count4}", org4, font, fontScale, color, thickness)
    cv2.putText(frame, f"{white_pixelsmid}    Max: {tmpmid} Time: {countmid}", orgmid, font, fontScale, color, thickness)

    cv2.line(frame, (0, int(height / 2)), (int(width), int(height / 2)), (0, 50, 255), 1)
    cv2.line(frame, (int(width / 2), 0), (int(width / 2), int(height)), (0, 50, 255), 1)

    cv2.putText(frame, f"Calibration: {calibration}", (width - 800, height - 20), font, fontScale, color, thickness)
    cv2.putText(frame, f"Focus: {focus}", (width - 800, height - 50), font, fontScale, color, thickness)

    cv2.imshow('frame', frame)
    cv2.imshow(window_name, frame)

    if keys == ord('c'):
        calibration = not calibration
    if keys == ord('f'):
        focus = not focus
    if keys == ord('q'):
        cv2.imwrite(os.path.join(IMAGE_SAVE_PATH, f'focus_{time.strftime("%Y%m%d-%H%M%S")}.jpg'), frame)
        with open(os.path.join(IMAGE_SAVE_PATH, f'data_{time.strftime("%Y%m%d-%H%M%S")}.txt'), 'w') as file:
            file.write(f"Upper left: {white_pixels1}    Max: {tmp1} Time: {count1}\n")
            file.write(f"Upper right: {white_pixels2}    Max: {tmp2} Time: {count2}\n")
            file.write(f"Lower left: {white_pixels3}    Max: {tmp3} Time: {count3}\n")
            file.write(f"Lower right: {white_pixels4}    Max: {tmp4} Time: {count4}\n")
            file.write(f"Mid: {white_pixelsmid}    Max: {tmpmid} Time: {countmid}\n")
        break
    if keys == ord('o'):
        name = sys.argv[1].split('_')
        dir_path = os.path.join(IMAGE_SAVE_PATH, f'{name[0]}/{name[1]}_{name[2]}')
        os.makedirs(dir_path, exist_ok=True)
        cv2.imwrite(os.path.join(dir_path, f'focus_{time.strftime("%Y%m%d-%H%M%S")}_{sys.argv[1]}.jpg'), frame)
        with open(os.path.join(dir_path, f'data_{time.strftime("%Y%m%d-%H%M%S")}.txt'), 'w') as file:
            file.write(f"Upper left: {white_pixels1}    Max: {tmp1} Time: {count1}\n")
            file.write(f"Upper right: {white_pixels2}    Max: {tmp2} Time: {count2}\n")
            file.write(f"Lower left: {white_pixels3}    Max: {tmp3} Time: {count3}\n")
            file.write(f"Lower right: {white_pixels4}    Max: {tmp4} Time: {count4}\n")
            file.write(f"Mid: {white_pixelsmid}    Max: {tmpmid} Time: {countmid}\n")
        capture_image(os.path.join(dir_path, f'image-{time.strftime("%Y%m%d-%H%M%S")}_{sys.argv[1]}.jpg'))
        break
    if keys == ord('r'):
        tmp1 = 0
        tmp2 = 0
        tmp3 = 0
        tmp4 = 0
        tmpmid = 0

cv2.destroyAllWindows()
