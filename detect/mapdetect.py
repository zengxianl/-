import cv2
import numpy as np
import os


def get_vertex(img):
    kernel = np.ones((1, 5), np.uint8)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = gray + 50
    ret, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel, anchor=(2, 0), iterations=5)
    contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(img, contours, -1, (0, 0, 255), 3)
    cv2.imshow("vertex", img)
    max_x = min_x = 250
    min_y = max_y = 250
    print(contours)
    for i in contours:
        for j in i:
            x = int(j[0][0])
            y = int(j[0][1])
            if x < 10 or x > 490 or y < 10 or y > 490:
                continue
            else:
                if max_y * max_y + max_x * max_x < x * x + y * y:
                    max_x = x
                    max_y = y
                if min_x * min_x + min_y * min_y > x * x + y * y:
                    min_y = y
                    min_x = x
    vertex = []
    vertex.append(max_x)
    vertex.append(max_y)
    vertex.append(min_x)
    vertex.append(min_y)
    with open("record.txt", 'a') as f:
        var = "max_x:" + str(max_x) + " max_y:" + str(max_y) + " min_x:" + str(min_x) + " min_y:" + str(min_y) + "\n"
        f.write(var)
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
                               param1=50, param2=30, minRadius=5, maxRadius=30)
    try:
        circles = np.uint16(np.around(circles))
    except:
        print("error in np convert")
    else:
        for i in circles[0, :]:
            # draw the outer circle
            # print(i)
            cv2.circle(enlarge, (i[0], i[1]), i[2], (255, 255, 0), 2)
            # draw the center of the circle
            cv2.circle(enlarge, (i[0], i[1]), 2, (255, 0, 0), 3)

        cv2.namedWindow("detected circles", cv2.WINDOW_FREERATIO)
        cv2.imshow('detected circles', enlarge)
        # cv2.imwrite("result-img/1.png", enlarge)
        # cv2.waitKey(1)
    return circles


def get_xys(circles, vertex):
    lens = vertex[0] - vertex[2]
    height = vertex[1] - vertex[3]
    dx = int(lens / 14)
    dy = int(height / 14)
    xys = []
    for i in circles[0]:
        i[0] = i[0] / 3
        i[1] = i[1] / 3
        with open("record.txt", 'a') as f:
            var = "x:" + str(i[0]) + " y:" + str(i[1]) + "\n"
            f.write(var)
    # print(circles[0])
    for i in circles[0]:
        xy = (int(i[0] / dx) - 3, int(i[1] / dy) - 3)
        with open("record.txt", 'a') as f:
            var = "normal x:" + str(xy[0]) + "normal y:" + str(xy[1]) + "\n"
            f.write(var)
        xys.append(xy)

    return xys


def main(src):
    xys = []
    xs = []
    ys = []
    img = src.copy()
    img = cv2.resize(img, (500, 500))
    cv2.imshow("img", img)
    vertex = get_vertex(img)
    print(vertex)
    # y:y x:x
    img = img[vertex[3]:vertex[1], vertex[2]:vertex[0]]
    img = cv2.resize(img, (500, 500))
    cv2.imshow("roi", img)
    circles = circle_detect(img)
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
        cv2.waitKey(0)


path = "./ori-img"
files = os.listdir(path)
for file in files:
    f = str(path + "/" + file)
    src = cv2.imread(f)
    main(src)
