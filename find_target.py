import win32gui

intended_res = (3440, 1440)
top_list, win_list = [], []


def enum_callback(hwnd, results):
    win_list.append((hwnd, win32gui.GetWindowText(hwnd)))


def main(target_title):
    win32gui.EnumWindows(enum_callback, top_list)

    # find the target window by title
    target = [(hwnd, title) for hwnd, title in win_list if target_title in title.lower()]
    if not target:
        print(f"Could not find window with title '{target_title}'")
        exit()

    return target[-1][0]
