import cv2
import numpy as np

# while cap.isOpened():
#     ret=True
#     frame=cv2.imread("imgs/calibresult.png")
#     if ret:
#         if frame is not None:
#             gs_frame = cv2.GaussianBlur(frame, (5, 5), 0)                     # 高斯模糊
#             hsv = cv2.cvtColor(gs_frame, cv2.COLOR_BGR2HSV)                 # 转化成HSV图像
#             erode_hsv = cv2.erode(hsv, None, iterations=2)                   # 腐蚀 粗的变细
#             inRange_hsv = cv2.inRange(erode_hsv, color_dist[ball_color]['Lower'], color_dist[ball_color]['Upper'])
#             cv2.imshow("inrange",inRange_hsv)
#             cnts = cv2.findContours(inRange_hsv.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
#
#             c = max(cnts, key=cv2.contourArea)
#             rect = cv2.minAreaRect(c)
#             box = cv2.boxPoints(rect)
#             cv2.drawContours(frame, [np.int0(box)], -1, (0, 255, 255), 2)
#
#             cv2.imshow('camera', frame)
#             cv2.waitKey(0)
# cap.release()
# cv2.waitKey(0)
# cv2.destroyAllWindows()
#
color_dist = {'red1': {'Lower': np.array([0, 43, 46]), 'Upper': np.array([10, 255, 255])},
              'red2': {'Lower': np.array([156, 43, 46]), 'Upper': np.array([180, 255, 255])},
              'blue': {'Lower': np.array([100, 43, 46]), 'Upper': np.array([124, 255, 255])},
              'green': {'Lower': np.array([35, 43, 46]), 'Upper': np.array([77, 255, 255])},
              'yellow': {'Lower': np.array([26, 43, 46]), 'Upper': np.array([34, 255, 255])},
              }


# color_dist = {'blue': {'Lower': np.array([100, 43, 46]), 'Upper': np.array([124, 255, 255])},
#               'yellow': {'Lower': np.array([26, 43, 46]), 'Upper': np.array([34, 255, 255])},
#               }


def color_read(mode, roi):
    if mode == 1:
        ball_color = 'red2'
    else:
        # 判断真假
        ball_color = 'green'
    gs_frame = cv2.GaussianBlur(roi, (5, 5), 0)  # 高斯模糊
    hsv = cv2.cvtColor(gs_frame, cv2.COLOR_BGR2HSV)  # 转化成HSV图像
    erode_hsv = cv2.erode(hsv, None, iterations=2)  # 腐蚀 粗的变细
    inRange_hsv = cv2.inRange(erode_hsv, color_dist[ball_color]['Lower'], color_dist[ball_color]['Upper'])
    cnts = cv2.findContours(inRange_hsv.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    if len(cnts) != 0:
        c = max(cnts, key=cv2.contourArea)
        rect = cv2.minAreaRect(c)
        box = cv2.boxPoints(rect)
        cv2.drawContours(roi, [np.intp(box)], -1, (0, 0, 0), 5)
        cv2.namedWindow("camera", cv2.WINDOW_FREERATIO)
        cv2.imshow('camera', roi)
        return True
    else:
        return False


img = cv2.imread("imgs/calibresult.png")
print((color_read(1, img)))
cv2.waitKey(0)
