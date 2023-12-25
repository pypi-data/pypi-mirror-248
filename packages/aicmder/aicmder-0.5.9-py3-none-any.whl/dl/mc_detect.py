import cv2
import numpy as np
from fence_detect import RotatedRect


def find_boxes(img):

    # threshold on black color
    lower = np.array([0, 0, 0])
    upper = np.array([100, 100, 100])
    mask = cv2.inRange(img, lower, upper)
    # plt.imshow(mask)
    # apply morphology
    kernel = np.ones((5, 5), np.uint8)
    morph = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    # find lines
    lines = cv2.HoughLinesP(morph, 1, np.pi/180, 100, minLineLength=100, maxLineGap=10)

    # draw lines on copy of input
    result = img.copy()
    # print(lines)
    x_left, x_right = 2000, 0
    for line in lines:
        x1, y1, x2, y2 = line[0]
        if x1 < x_left:
            x_left = x1
        if x2 > x_right:
            x_right = x2
        cv2.line(result, (x1, y1), (x2, y2), (0, 255, 0), 3)
    h, w, _ = img.shape
    print(x_left, x_right, h, w)
    box_w = (x_right - x_left) // 10
    box_h = h
    boxes = []
    for i in range(10):
        boxes.append({
            "start_x": (x_left + i * box_w),
            "end_x": (x_left + (i + 1) * box_w),
            "start_y": 0,
            "end_y": box_h
        })
    # print(boxes)
    return boxes


def match_ans_with_boxes(mc_data, boxes_data, iouThreshold=0.8):
    boxes = []
    for obj in boxes_data:
        start_x, end_x, end_y, start_y = obj["start_x"], obj["end_x"], obj["end_y"], obj["start_y"]
        width = end_x - start_x
        height = end_y - start_y
        center_x = start_x + width / 2
        center_y = start_y + height / 2

        obj_rect = RotatedRect()
        obj_rect.set_param(center_x, center_y, width, height, 0)
        boxes.append(obj_rect)

    ans = []
    for j, obj in enumerate(mc_data):
        start_x, end_x, end_y, start_y = obj["start_x"], obj["end_x"], obj["end_y"], obj["start_y"]
        width = end_x - start_x
        height = end_y - start_y
        center_x = start_x + width / 2
        center_y = start_y + height / 2

        obj_rect = RotatedRect()
        obj_rect.set_param(center_x, center_y, width, height, 0)

        for i, box in enumerate(boxes):
            if obj_rect.occlusion_rate(box) >= iouThreshold:
                ans.append(((i + 1), obj))
                break
    return ans
