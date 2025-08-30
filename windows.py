from base import MouseController

import win32api, win32con

class WindowsMouseController(MouseController):
    def __init__(self):
        super().__init__()

    def click(self):
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

    def detectInterrupt(self):
        return win32api.GetAsyncKeyState(win32con.VK_RBUTTON)