from base import Controller

import win32api, win32con

class WindowsController(Controller):
    def __init__(self):
        super().__init__()

    def click_keyboard(self, button_list):
        for button in button_list:
            win32api.keybd_event(ord(button), 0, 0, 0)  # Key down
            win32api.keybd_event(ord(button), 0, win32con.KEYEVENTF_KEYUP, 0)  # Key up

    def click_left(self):
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

    def detectRightclick(self):
        return win32api.GetAsyncKeyState(win32con.VK_RBUTTON)
