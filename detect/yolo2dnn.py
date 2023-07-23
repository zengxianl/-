import numpy as np
import cv2


class yolo2dnn:
    def __init__(self, onnxNet, txtPath):
        self.target = None
        self.net = cv2.dnn.readNet(onnxNet)
        with open(txtPath, "r") as f:
            self.class_list = [cname.strip() for cname in f.readlines()]

    def format_yolov5(self, frame):
        row, col, _ = frame.shape
        _max = max(col, row)
        result = np.zeros((_max, _max, 3), np.uint8)
        result[0:row, 0:col] = frame
        return result

    def main_process(self, src):
        self.img = src.copy()
        input_image = self.format_yolov5(self.img)  # making the image square
        blob = cv2.dnn.blobFromImage(input_image, 1 / 255.0, (640, 640), swapRB=True)
        self.net.setInput(blob)
        predictions = self.net.forward()

        class_ids = []
        confidences = []
        boxes = []

        output_data = predictions[0]

        image_width, image_height, _ = input_image.shape
        x_factor = image_width / 640
        y_factor = image_height / 640

        for r in range(25200):
            row = output_data[r]
            confidence = row[4]
            if confidence >= 0.4:

                classes_scores = row[5:]
                _, _, _, max_index = cv2.minMaxLoc(classes_scores)
                class_id = max_index[1]
                if classes_scores[class_id] > .25:
                    confidences.append(confidence)

                    class_ids.append(class_id)

                    x, y, w, h = row[0].item(), row[1].item(), row[2].item(), row[3].item()
                    left = int((x - 0.5 * w) * x_factor)
                    top = int((y - 0.5 * h) * y_factor)
                    width = int(w * x_factor)
                    height = int(h * y_factor)
                    box = np.array([left, top, width, height])
                    boxes.append(box)

        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.25, 0.45)

        result_class_ids = []
        result_confidences = []
        result_boxes = []

        for i in indexes:
            result_confidences.append(confidences[i])
            result_class_ids.append(class_ids[i])
            result_boxes.append(boxes[i])

        for i in range(len(result_class_ids)):
            self.target = result_boxes[i]
            class_id = result_class_ids[i]

            cv2.rectangle(self.img, box, (0, 0, 255), 2)
            cv2.rectangle(self.img, (self.target[0], self.target[1] - 20), (self.target[0] + self.target[2], self.target[1]), (0, 255, 255), -1)
            cv2.putText(self.img, self.class_list[class_id], (self.target[0], self.target[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, .5,
                        (0, 0, 0))
            # cv2.imshow("detect",self.img)
            # cv2.waitKey(1000)


# src1 = cv2.imread("./2.JPG")
# if src1 is None:
#     print("error in img")
# detect = yolo2dnn('./best.onnx', "./map.txt")
#
# detect.main_process(src1)
# print(detect.target)
# cv2.imshow("output", detect.img)
# cv2.waitKey(0)
