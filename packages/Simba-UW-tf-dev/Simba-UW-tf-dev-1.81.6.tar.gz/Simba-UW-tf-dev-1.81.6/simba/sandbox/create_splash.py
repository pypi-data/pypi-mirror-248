import cv2
import numpy as np
from simba.utils.enums import Formats
import imutils

LENGTH_S = 3
FPS = 20
IMAGE_PATH = '/Users/simon/Desktop/splash_2024.png'
ALPHA = list(range(0, 105, 2))
FRAME_COUNT = int(FPS * LENGTH_S)
SAVE_PATH = '/Users/simon/Desktop/splash_2024.mp4'
for i in range(FRAME_COUNT-len(ALPHA)): ALPHA.append(100)
fourcc = cv2.VideoWriter_fourcc(*Formats.MP4_CODEC.value)


original_img = cv2.imread(IMAGE_PATH)
white_image = np.ones((original_img.shape[0], original_img.shape[1], 3), dtype=np.uint8) * 255
writer = cv2.VideoWriter(SAVE_PATH, fourcc, FPS, (original_img.shape[1], original_img.shape[0]))

for frm_cnt in range(int(FPS * LENGTH_S)):
    current_image = np.copy(original_img)
    img_alpha = ALPHA[frm_cnt] / 100
    blended = cv2.addWeighted(white_image, 1 - img_alpha, original_img, img_alpha, 0).astype(np.uint8)
    img = imutils.resize(blended, width=800)
    writer.write(blended)
    #cv2.waitKey(33)

writer.release()


