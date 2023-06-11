import cv2
def color_diff(img):
    cols = img.shape[0]
    rows = img.shape[1]
    bgr = img[int(cols / 2), int(rows / 2)]
    b = bgr[0]
    g = bgr[1]
    r = bgr[2]
    if (b > r):
        print("blue")
    else:
        print("red")


def fake_det(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

    contours, hierarchy = cv2.findContours(binary, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    a=len(contours)
    if(a>4):
        print("fake")
    else:
        print("true")