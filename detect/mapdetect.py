from PIL import Image
import cv2
import matplotlib.pyplot as plt
import numpy as np


def get_vertex(img):
    kernel = np.ones((1, 5), np.uint8)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel, anchor=(2, 0), iterations=5)
    contours, hierarchy = cv2.findContours(binary, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(img, contours, -1, (0, 255, 255), 1)
    max_x = min_x = 250
    min_y = max_y = 250
    for i in contours:
        for j in i:
            x = int(j[0][0])
            y = int(j[0][1])
            if x < 20 or x > 480 or y < 20 or y > 490:
                continue
            else:
                max_x = x if x > max_x else max_x
                max_y = y if y > max_y else max_y
                min_x = x if x < min_x else min_x
                min_y = y if y < min_y else min_y
    vertex = []
    vertex.append(max_x)
    vertex.append(max_y)
    vertex.append(min_x)
    vertex.append(min_y)
    return vertex


def draw_circle(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        print(x, y)


def get_xy(img):
    # Create a black image, a window and bind the function to window
    dst = cv2.resize(img, (500, 500))
    cv2.namedWindow('image')
    cv2.setMouseCallback('image', draw_circle)

    while (1):
        cv2.imshow('image', dst)
        if cv2.waitKey(20) & 0xFF == 27:
            break
    cv2.destroyAllWindows()


def circle_detect(img):
    circles = np.array([])
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    enlarge = cv2.resize(gray, (0, 0), fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
    circles = cv2.HoughCircles(enlarge, cv2.HOUGH_GRADIENT, 1.027, 20,
                               param1=50, param2=30, minRadius=5, maxRadius=50)
    print(type(circles))
    try:
        circles = np.uint16(np.around(circles))
    except:
        print("error in np convert")
        print(type(circles))
    else:
        for i in circles[0, :]:
            # draw the outer circle
            # print(i)
            cv2.circle(enlarge, (i[0], i[1]), i[2], (255, 255, 0), 2)
            # draw the center of the circle
            cv2.circle(enlarge, (i[0], i[1]), 2, (255, 0, 0), 3)
        cv2.namedWindow("detected circles", cv2.WINDOW_FREERATIO)
        cv2.imshow('detected circles', enlarge)
        # cv2.imwrite("img_det.png", enlarge)
        cv2.waitKey(1)
    return circles


def get_xys(circles, vertex):
    lens = vertex[0] - vertex[2]
    height = vertex[1] - vertex[3]
    # print(lens)
    # print(height)
    dx = int(lens / 14)
    dy = int(height / 14)
    xys = []
    for i in circles[0]:
        i[0] = i[0] / 3
        i[1] = i[1] / 3
    # print(circles[0])
    for i in circles[0]:
        xy = (int(i[0] / dx) - 3, int(i[1] / dy) - 3)
        xys.append(xy)
    return xys


def main(src):
    xys = []
    xs = []
    ys = []
    img = src.copy()
    img = cv2.resize(img, (500, 500))
    cv2.imshow("img", img)
    circles = circle_detect(img)
    vertex = get_vertex(img)
    try:
        len(circles)
    except:
        print("circle in error")
    else:
        xys = get_xys(circles, vertex)
        if len(xys) == 8:
            for items in xys:
                xs.append(items[0])
                ys.append(items[1])
            print("get 8 points")


# src = cv2.imread("./imgs/img.png")
# main(src)
