import threading
import queue
import time

class PyTimer:
    """定时器类"""

    def __init__(self, func, *args, **kwargs):
        """构造函数"""

        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.running = False

    #def _run_func(self):
        """运行定时事件函数"""

        #th = threading.Thread(target=self.func, args=self.args, kwargs=self.kwargs)
        #th.setDaemon(True)
        #th.start()

    def _start(self, interval, once):
        """启动定时器的线程函数"""

        if once:
            if interval < 0.010:
                interval = 0.010

            if interval < 0.050:
                dt = interval / 10
            else:
                dt = 0.005
            deadline = time.time() + interval
            while time.time() < deadline:
                time.sleep(dt)

            # 定时时间到，调用定时事件函数
            #self._run_func()
            self.func()
        else:
            self.running = True
            while self.running:
                if interval < 0.010:
                    interval = 0.010

                if interval < 0.050:
                    dt = interval / 10
                else:
                    dt = 0.005
                deadline = time.time() + interval
                while time.time() < deadline:
                    time.sleep(dt)

                # 更新下一次定时时间
                deadline += interval

                # 定时时间到，调用定时事件函数
                if self.running:
                    #self._run_func()
                    self.func()

    def start(self, interval, once=False):
        """启动定时器

        interval    - 定时间隔，浮点型，以秒为单位，最高精度10毫秒
        once        - 是否仅启动一次，默认是连续的
        """

        th = threading.Thread(target=self._start, args=(interval, once))
        #th.setDaemon(True)
        th.start()

    def stop(self):
        """停止定时器"""
        self.running = False