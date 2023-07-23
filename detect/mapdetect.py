import cv2
import numpy as np
import time
import math
from yolo2dnn import yolo2dnn
import os

color_dist = {'red1': {'Lower': np.array([0, 43, 46]), 'Upper': np.array([10, 255, 255])},
              'red2': {'Lower': np.array([156, 43, 46]), 'Upper': np.array([180, 255, 255])},
              'blue': {'Lower': np.array([100, 43, 46]), 'Upper': np.array([124, 255, 255])},
              'green': {'Lower': np.array([35, 43, 46]), 'Upper': np.array([77, 255, 255])},
              'yellow': {'Lower': np.array([26, 43, 46]), 'Upper': np.array([34, 255, 255])},
              }

color_mode = {1: 'blue', 2: 'red1', 3: 'red2', 4: 'green', 5: 'yellow'}


def color_read(mode, roi):
    ball_color = color_mode[mode]
    print(ball_color)
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


def get_vertex(img):
    """

    Args:
        img: 输入一张图片

    Returns:返回四个角点

    """
    points = []
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 200)
    contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        center, (width, height), angle = cv2.minAreaRect(contour)
        if -8 <= (width - height) <= 8 and 30 <= width <= 60:
            cv2.drawContours(img, [contour], -1, (0, 0, 255), 1)
            points.append(center)
    cv2.imshow("vertex", img)
    max_x = min_x = 250
    min_y = max_y = 250
    left_botx = 250
    left_boty = 250
    right_topx = 250
    right_topy = 250
    for i in points:
        x = int(i[0])
        y = int(i[1])
        if x < 10 or x > 490 or y < 10 or y > 490:
            continue
        else:
            if max_y * max_y + max_x * max_x < x * x + y * y:
                max_x = x
                max_y = y
            if min_x * min_x + min_y * min_y > x * x + y * y:
                min_y = y
                min_x = x
            if x < left_botx and y > left_boty:
                left_botx = x
                left_boty = y
            if x > right_topx and y < right_topy:
                right_topy = y
                right_topx = x

    '''
    left-top:minx,miny
    right-top:maxx,miny
    left-bot:minx,maxy
    right-bot:maxx,maxy
    '''
    left_top = (min_x - 15, min_y - 15)
    right_bot = (max_x + 15, max_y + 15)
    right_top = (right_topx + 15, right_topy - 15)
    left_bot = (left_botx - 15, left_boty + 15)
    vertex = [left_top, right_top, left_bot, right_bot]
    return vertex


def get_xys(img):
    """

    Args:
        img: 输入一张图片

    Returns:返回圆点的位置和半径

    """
    circle_f = []
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    enlarge = cv2.resize(gray, (0, 0), fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
    circles = cv2.HoughCircles(enlarge, cv2.HOUGH_GRADIENT, 1.027, 20,
                               param1=50, param2=30, minRadius=5, maxRadius=30)
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            if i[0] < 100 or i[0] > 1400:
                continue
            circle_f.append(i)
        for i in circle_f:
            cv2.circle(enlarge, (i[0], i[1]), i[2], (255, 255, 0), 2)
            cv2.circle(enlarge, (i[0], i[1]), 2, (255, 0, 0), 3)
        cv2.namedWindow("detected circles", cv2.WINDOW_FREERATIO)
        cv2.imshow('detected circles', enlarge)
    dx = int(1500 / 14)
    dy = int(1500 / 14)
    # opencv里面的xy
    xys = []
    # i[0]--x,i[1]--y
    # print(circles)
    for i in circle_f:
        # print(i)
        xy = (math.ceil(i[0] / dx) - 2, math.ceil(i[1] / dy) - 2)
        if 11 > xy[0] > -1 and 11 > xy[1] > -1:
            xys.append(xy)
    return xys


def myWarpPerspective(img, vertex):
    # print(vertex)
    pts1 = np.float32([vertex[0], vertex[1], vertex[2], vertex[3]])
    pts2 = np.float32([[0, 0], [500, 0], [0, 500], [500, 500]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    return cv2.warpPerspective(img, matrix, (500, 500))


def get_x_y(src):
    """

    Args:
        src: 输入图片

    Returns:输出宝藏的xy值

    """
    xs = []
    ys = []
    img = src.copy()
    if img is None or img.shape[0] == 0 or img.shape[1] == 0:
        print("none")
        return xs, ys
    img = cv2.resize(img, (500, 500))
    cv2.imshow("img", img)
    vertex = get_vertex(img)
    img = myWarpPerspective(img, vertex)
    if img is None or img.shape[0] == 0 or img.shape[1] == 0:
        print("none")
        return xs, ys

    img2 = cv2.resize(img, (500, 500))
    cv2.imshow("wp", img2)
    print(img2[100, 450])
    # B-0 R-1
    color = 0 if img2[100, 450, 0] > img2[100, 450, 2] else 1
    xys = get_xys(img2)
    xys.sort()
    for items in xys:
        xs.append(items[0])
        ys.append(items[1])
    cv2.waitKey(1)
    return xs, ys, color


def treasure(src, selfcolor):
    # 0-B 1-R
    go = 0
    img = src.copy()
    if img is None or img.shape[0] == 0 or img.shape[1] == 0:
        print("none")
    img2 = cv2.resize(img, (500, 500))
    roi = img2[250:500, 100:400].copy()
    color = 0 if color_read(1, roi) else 1
    print(color)
    if color == selfcolor:
        # B-selfcolor
        if selfcolor == 0:
            go = 1 if color_read(5, roi) else 0
        # R--selfcolor
        if selfcolor == 1:
            go = 1 if color_read(4, roi) else 0
    return go


# def main():
#     path = "./ori-img"
#     files = os.listdir(path)
#     for file in files:
#         f = str(path + "/" + file)
#         src = cv2.imread(f)
#         print(f)
#         xs, ys = get_x_y(src)
#         if len(xs) != 8:
#             print("error")
#         else:
#             print(xs)
#             print(ys)

# def main():
#     cap = cv2.VideoCapture(0)
#     while True:
#         # 一帧一帧捕捉
#         ret, frame = cap.read()
#         xs, ys, color = get_x_y(frame)
#         if len(xs) != 8:
#             print("error")
#         else:
#             print(xs)
#             print(ys)
#             print(color)
#             cv2.waitKey(0)

def main():
    src = cv2.imread("1.png")
    cv2.imshow("src", src)
    img = cv2.resize(src, (500, 500))
    if img is None:
        print("error")
    img = img[0:500, 0:250]
    cv2.imshow("img", img)
    print(treasure(img, 0))
    cv2.waitKey(0)


if __name__ == '__main__':
    main()
