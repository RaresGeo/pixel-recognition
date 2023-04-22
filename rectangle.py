import tkinter as tk

import win32gui


def center_window(window, width, height, bbox=None):
    if bbox is None:
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
    else:
        left, top, right, bottom = bbox
        screen_width = right - left
        screen_height = bottom - top

    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)

    if bbox is None:
        window.geometry('%dx%d+%d+%d' % (width, height, x, y))
    else:
        window.geometry('%dx%d+%d+%d' % (width, height, left + x, top + y))


def main(hwnd, message_queue):
    window_width = 200
    window_height = 200

    root = tk.Tk()
    root.title("Target Area")
    root.attributes("-topmost", True)  # Keep the window on top
    root.overrideredirect(1)  # Remove the window border
    root.wm_attributes("-transparentcolor", "white")

    canvas = tk.Canvas(root, bg='white', bd=0, highlightthickness=0, width=window_width, height=window_height)

    canvas.pack()

    # Draw a square with a transparent center and a red outline
    # Draw a red rectangle as the highlight if paused, white otherwise
    rectangle_id = canvas.create_rectangle(0, 0, window_width, window_height, fill='white',
                                           outline='black',
                                           width=10)

    def update_paused_state():
        while not message_queue.empty():
            paused = message_queue.get()
            canvas.itemconfig(rectangle_id, outline='red' if paused else 'black')

        root.after(100, update_paused_state)

    if hwnd is not None:
        bbox = win32gui.GetWindowRect(hwnd)
        center_window(root, window_width, window_height, bbox)
    else:
        center_window(root, window_width, window_height)

    update_paused_state()

    root.mainloop()


if __name__ == "__main__":
    # Pass an hwnd to main to center the window inside its bounding box
    main(None)
