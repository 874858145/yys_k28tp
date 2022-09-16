import sys
import time

from yys_k28tp_ui_main import *
from yys_k28tp_screen import *
from yys_k28tp_mouse import *
from yysk28tp_yolov5m import *
from PyTimer import *
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # 使用ui文件导入定义界面类
        self.ui = Ui_MainWindow()
        # 初始化界面
        self.ui.setupUi(self)

        #self.ui.Btn_Recognition.clicked.connect(self.btn_recognition_onclicked)

        self.hwnd = win32gui.FindWindow(None, "阴阳师-网易游戏")
        self.screen = Screen(hwnd=self.hwnd)
        self.mouse = Mouse(hwnd=self.hwnd)

        self.res = None

        self.net = Yolov5('./weights/yolov5m-yys-sim.onnx', './yys_k28tp.names', 0.5, 0.7)

        self.timer = PyTimer(self.yolov5_recognition)
        self.timer.start(0.025, once=False)

    @staticmethod
    def resize_image(srcimg, imgh, imgw, keep_ratio=True):
        if keep_ratio and srcimg.shape[0] != srcimg.shape[1]:
            hw_scale = srcimg.shape[0] / srcimg.shape[1]
            if hw_scale > 1:
                newh, neww = imgh, int(imgw / hw_scale)
                img = cv2.resize(srcimg, (neww, newh), interpolation=cv2.INTER_AREA)
                #left = int((imgw - neww) * 0.5)
                #img = cv2.copyMakeBorder(img, 0, 0, left, imgw - neww - left, cv2.BORDER_CONSTANT, value=0)  # add border
            else:
                newh, neww = int(imgh * hw_scale), imgw
                img = cv2.resize(srcimg, (neww, newh), interpolation=cv2.INTER_AREA)
                #top = int((imgh - newh) * 0.5)
                #img = cv2.copyMakeBorder(img, top, imgh - newh - top, 0, 0, cv2.BORDER_CONSTANT, value=0)
        else:
            img = cv2.resize(srcimg, (imgh, imgw), interpolation=cv2.INTER_AREA)
        return img

    # 搜索列表里时候有相同的classid
    def yolov5_index(self, ress, classid):
        outs = []
        for res in ress:
            if res[4] == classid:
                outs.append(res)
        return outs

    def yolov5_recognition(self):
        if not self.hwnd:
            print('未找到窗口！！')
            time.sleep(10)
            self.hwnd = win32gui.FindWindow(None, "阴阳师-网易游戏")
            self.screen = Screen(hwnd=self.hwnd)
            self.mouse = Mouse(hwnd=self.hwnd)
        else:
            img = self.screen.capture()
            if img is not None:
                img, self.res = self.net.detect(img)
                #print(self.res)

                img = self.resize_image(img, int(self.ui.L_cvImage.height() / 4) * 4,
                                        int(self.ui.L_cvImage.width() / 4) * 4)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                img = QImage(img.data, img.shape[1], img.shape[0], QImage.Format_RGB888)
                self.ui.L_cvImage.setPixmap(QPixmap.fromImage(img))
                # self.ui.L_cvImage.setScaledContents(True)  #图片自适应大小
                self.ui.L_cvImage.show()
            else:
                print('截图失败！！')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = MainWindow()
    MainWindow.show()
    sys.exit(app.exec_())
