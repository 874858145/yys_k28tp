import sys

import win32gui
import win32con
import win32api
import ctypes
import time
import random


class Mouse:
    def __init__(self, win_title=None, win_class=None, hwnd=None) -> None:
        self.bind(win_title, win_class, hwnd)

    def bind(self, win_title=None, win_class=None, hwnd=None):
        '可以直接传入句柄，否则就根据class和title来查找，并把句柄做为实例属性 self._hwnd'
        if not hwnd:
            self._hwnd = win32gui.FindWindow(win_class, win_title)
        else:
            self._hwnd = hwnd

    # 单击
    def oneclick(self, cx, cy):
        point = win32api.MAKELONG(cx, cy)  # 模拟鼠标指针 传送到指定坐标
        win32api.SendMessage(self._hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, point)  # 模拟鼠标按下
        t1 = random.uniform(0.1, 0.5)
        time.sleep(t1)
        win32api.SendMessage(self._hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, point)  # 模拟鼠标弹起

    # 拖动
    def drag(self, cx1, cy1, cx2, cy2):
        point1 = win32api.MAKELONG(cx1, cy1)  # 模拟鼠标指针 传送到指定坐标
        point2 = win32api.MAKELONG(cx2, cy2)  # 模拟鼠标指针 传送到指定坐标
        win32api.SendMessage(self._hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, point1)  # 模拟鼠标按下
        win32api.SendMessage(self._hwnd, win32con.WM_MOUSEMOVE, win32con.MK_LBUTTON, point2)
        win32api.SendMessage(self._hwnd, win32con.WM_LBUTTONUP, 0, 0)  # 模拟鼠标弹起


if __name__ == '__main__':
    if not ctypes.windll.shell32.IsUserAnAdmin():
        # 不是管理员就提权
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, __file__, None, 1)

    # 获取窗口截图
    # screen = Screen(win_title='阴阳师-网易游戏')
    # img = screen.capture()
    # if img is not None:
    #    cv2.imshow("image",img)      #imshow

    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # 获取windows窗口的标题和类名
    # winct = WinClassAndTitle()
    # print(winct.getAllWindows())

    # handle = win32gui.FindWindow(None, "阴阳师-网易游戏")
    handle = win32gui.FindWindow(None, '计算器')
    # 左上角和右下角
    window_post = win32gui.GetWindowRect(handle)
    print(window_post)

    Mouse = Mouse(hwnd=handle)
    Mouse.oneclick(50, 400)
