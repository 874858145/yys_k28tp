from PyQt5.QtWidgets import QApplication
import sys
import cv2
import numpy as np

import win32gui
import win32con
import win32api
import ctypes
import time
import random


# 直接写一个类，方便以后使用
class Screen:
    def __init__(self, win_title=None, win_class=None, hwnd=None) -> None:
        self.app = QApplication(['WindowCapture'])
        self.screen = QApplication.primaryScreen()
        self.bind(win_title, win_class, hwnd)

    def bind(self, win_title=None, win_class=None, hwnd=None):
        '可以直接传入句柄，否则就根据class和title来查找，并把句柄做为实例属性 self._hwnd'
        if not hwnd:
            self._hwnd = win32gui.FindWindow(win_class, win_title)
        else:
            self._hwnd = hwnd

    def convertQImageToMat(self, incomingImage):
        '''  Converts a QImage into an opencv MAT format  '''
        # Format_RGB32 = 4,存入格式為B,G,R,A 對應 0,1,2,3
        # RGB32圖像每個像素用32比特位表示，占4個字節，
        # R，G，B分量分別用8個bit表示，存儲順序為B，G，R，最後8個字節保留
        incomingImage = incomingImage.convertToFormat(4)
        width = incomingImage.width()
        height = incomingImage.height()

        ptr = incomingImage.bits()
        ptr.setsize(incomingImage.byteCount())
        arr = np.array(ptr).reshape(height, width, 4)  # Copies the data
        # arr為BGRA，4通道圖片
        return arr

    def capture(self):
        self.img = self.screen.grabWindow(self._hwnd).toImage()
        if self.img is not None:
            self.img = self.convertQImageToMat(self.img)
        return self.img


# 获取windows窗口的标题和类名
class WinClassAndTitle:
    def __init__(self):
        self.winct_list = []
        self.windows_list = []

    def getAllWindows(self):
        win32gui.EnumWindows(lambda hWnd, param: param.append(hWnd), self.windows_list)
        for window in self.windows_list:
            if win32gui.IsWindow(window) and win32gui.IsWindowEnabled(window) and win32gui.IsWindowVisible(window):
                self.winct_list.append([win32gui.GetClassName(window), win32gui.GetWindowText(window)])
        return self.winct_list


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
