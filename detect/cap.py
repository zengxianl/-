# coding:utf-8
import cv2
import numpy as np
import preprocess
import mapdetect

def main():
    cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
    flag = cap.isOpened()
    index = 1
    while (flag):
        print("camera is opened")
        ret, frame = cap.read()
        cv2.imshow("ori", frame)
        mtx = np.load("./param/mtx.npy")
        dist = np.load("./param/dist.npy")
        corrected=preprocess.imgcorrect(frame, mtx, dist)

        mapdetect.main(frame)

        cv2.imshow("corrected",corrected)


        cv2.waitKey(1)
    cap.release() # 释放摄像头
    cv2.destroyAllWindows()# 释放并销毁窗口
main()