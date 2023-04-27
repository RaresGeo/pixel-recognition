import cv2
import numpy as np

blue_lower = np.array([85, 130, 200])
blue_upper = np.array([105, 255, 255])
green_lower = np.array([40, 50, 50])
green_upper = np.array([90, 255, 255])


def count_pixels(pil_img, color):
    # Convert PIL image to OpenCV image format
    opencv_img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

    # Convert BGR to HSV
    hsv = cv2.cvtColor(opencv_img, cv2.COLOR_BGR2HSV)

    # Define color ranges
    lower = np.array(color[0])
    upper = np.array(color[1])

    # Threshold the HSV image to get only blue and green colors
    mask = cv2.inRange(hsv, lower, upper)

    # Calculate the number of blue and green pixels
    pixels = cv2.countNonZero(mask)

    return pixels


def detect_fishing_state(pil_img):
    blue_pixels = count_pixels(pil_img, (blue_lower, blue_upper))
    green_pixels = count_pixels(pil_img, (green_lower, green_upper))

    if blue_pixels > green_pixels:
        if blue_pixels > 0:
            return 1
        else:
            return 0
    else:
        if green_pixels > 0:
            return 2
        else:
            return 0


def detect_fish_meter(pil_img):
    # Define color ranges
    green_pixels = count_pixels(pil_img, (green_lower, green_upper))

    return green_pixels
