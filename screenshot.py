import win32api
import win32gui
from PIL import ImageGrab

intended_res = (3440, 1440)

minigame_offset = 40
minigame_height = 21
minigame_width = 300


def get_corrected_bbox(hwnd):
    # convert the client rectangle to screen coordinates
    (left, top, right, bottom) = win32gui.GetWindowRect(hwnd)
    screen_metrics = (win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1))
    # Account for scaling by multiplying each edge by the ratio of the intended resolution to the screen metrics
    left = int(left * intended_res[0] / screen_metrics[0])
    top = int(top * intended_res[1] / screen_metrics[1])
    right = int(right * intended_res[0] / screen_metrics[0])
    bottom = int(bottom * intended_res[1] / screen_metrics[1])
    bbox = (left, top, right, bottom)
    return bbox


def game_one(hwnd):
    bbox = get_corrected_bbox(hwnd)
    img = ImageGrab.grab(bbox)
    return img


def game_two(hwnd):
    bbox = get_corrected_bbox(hwnd)
    (left, top, right, bottom) = bbox

    new_left = (right + left) / 2 - (minigame_width / 2)
    new_top = bottom - minigame_offset - minigame_height / 2 - 1
    new_right = (right + left) / 2 + (minigame_width / 2)
    new_bottom = bottom - minigame_offset - minigame_height / 2 + 1
    bbox = (new_left, new_top, new_right, new_bottom)

    print(f"New Window rectangle: {bbox}")
    img = ImageGrab.grab(bbox)
    # img.save("output/screenshot.png")
    return img
