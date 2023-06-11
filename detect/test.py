import cv2


for i in range(1):
    e = cv2.imread("img.png")
    g = cv2.cvtColor(e, cv2.COLOR_BGR2GRAY)
    r, b = cv2.threshold(g, 0, 255, cv2.THRESH_OTSU)
    cr, t = cv2.findContours(b, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    ep = 0.01 * cv2.arcLength(cr[1], True)
    ap = cv2.approxPolyDP(cr[1], ep, True)
    co = len(ap)
    if co == 3:
        st = '三角形'
    elif co == 4:
        st = '矩形'
    elif co == 10:
        st = '五角星'
    else:
        st = '圆'
    print(st)
