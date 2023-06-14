# coding:utf-8
import cv2
import numpy as np
import preprocess
import mapdetect


def fun():
    cap = cv2.VideoCapture(0)
    while True:
        # 一帧一帧捕捉
        ret, frame = cap.read()
        # 显示返回的每帧
        cv2.imshow('frame', frame)
        img=frame.copy()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        mtx = np.load("./param/mtx.npy")
        dist = np.load("./param/dist.npy")
        #corrected=preprocess.imgcorrect(img, mtx, dist)

        mapdetect.main(img)

        #cv2.imshow("corrected",corrected)


        cv2.waitKey(1)
    # 当所有事完成，释放 VideoCapture 对象
    cap.release()
    cv.destroyAllWindows()


fun()