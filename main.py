import asyncio
import random
import threading
from queue import Queue
from datetime import datetime

import keyboard
import win32gui

from detect import detect_fishing_state, detect_fish_meter
from find_target import main as find_target
from rectangle import main as rectangle
from screenshot import game_one, game_two
from simulate_input import main as simulate_input

target_title = "target area"
rage_title = "rage multiplayer"


def random_float_within_range(x):
    return random.uniform(x * 0.9, x * 1.1)


def is_rage_window_active(hwnd, paused):
    active_hwnd = win32gui.GetForegroundWindow()
    return active_hwnd == hwnd and not paused


def main():
    paused = False
    loop = asyncio.get_event_loop()
    message_queue = Queue()

    print("Press F5 to start the rectangle window")
    keyboard.wait('f5')

    active_hwnd = win32gui.GetForegroundWindow()
    active_window_title = win32gui.GetWindowText(active_hwnd)

    print(f"Target is: {active_window_title}, {active_hwnd}, started at {datetime.now().strftime('%H:%M:%S')}")
    # Start the rectangle window, pass active_hwnd to it
    t1 = threading.Thread(target=rectangle, args=(active_hwnd, message_queue))

    t1.start()

    loop.run_until_complete(asyncio.sleep(1))

    target_hwnd = find_target(target_title)
    rage_hwnd = active_hwnd

    # img_game_one = game_one(target_hwnd)
    # state = detect_fishing_state(img_game_one)
    # print(f"State: {state}")

    # img_game_two = game_two(rage_hwnd)
    # green_pixels = detect_fish_meter(img_game_two)
    # print(f"Green pixels: {green_pixels}")
    
    # if rage_hwnd != 169:
    #     return

    # Take a screenshot of the target area once every 500ms
    while True:
        # If F6 is pressed, pause
        if keyboard.is_pressed('f6'):
            paused = not paused
            print(f"{'Paused' if paused else 'Resumed'}")
            message_queue.put(paused)
            loop.run_until_complete(asyncio.sleep(random_float_within_range(1)))
            continue
        # Check if the active window is the rage window
        if is_rage_window_active(rage_hwnd, paused):
            loop.run_until_complete(asyncio.sleep(random_float_within_range(0.25)))
        else:
            continue

        img_game_one = game_one(target_hwnd)
        state = detect_fishing_state(img_game_one)
        if state == 2:
            started_second_phase = True
            simulate_input()
            # Print current datetime
            print(f"Fish detected at {datetime.now().strftime('%H:%M:%S')}")
            # If everything went right, we should have a fish meter here now
            while True:
                if keyboard.is_pressed('f6'):
                    paused = not paused
                    print(f"{'Paused' if paused else 'Resumed'}")
                    message_queue.put(paused)
                    loop.run_until_complete(asyncio.sleep(random_float_within_range(1)))
                    continue
                # Check if the active window is the rage window
                if is_rage_window_active(rage_hwnd, paused):
                    loop.run_until_complete(asyncio.sleep(random_float_within_range(0.05)))
                else:
                    continue

                img_game_two = game_two(rage_hwnd)
                green_pixels = detect_fish_meter(img_game_two)
                if green_pixels == 0:
                    if started_second_phase:
                        # Check if the active window is the rage window
                        if is_rage_window_active(rage_hwnd, paused):
                            loop.run_until_complete(asyncio.sleep(random_float_within_range(0.25)))
                            started_second_phase = False
                            continue
                        else:
                            continue
                    else:
                        break
                if 35 > green_pixels > 0:
                    simulate_input()
                    # Print current datetime
                    print(f"Caught a fish at {datetime.now().strftime('%H:%M:%S')}")
                    break
        elif state == 0:
            simulate_input()


if __name__ == "__main__":
    main()
