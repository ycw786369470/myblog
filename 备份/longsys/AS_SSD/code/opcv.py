import win32gui
import win32con
import  random
from win32gui import *
import time

while True:
    titles = set()
    def foo(hwnd, Nouse):
            titles.add(GetWindowText(hwnd))
    EnumWindows(foo, 0)
    if "AS SSD Benchmark" in titles:
        QQwin = win32gui.FindWindow("TXGuiFoundation", "AS SSD Benchmark")
        x = random.randrange(1900)
        y = random.randrange(1200)
        win32gui.ShowWindow(QQwin, win32con.SW_HIDE)  # 隐藏
        time.sleep(1)  # 持续时间
        win32gui.ShowWindow(QQwin, win32con.SW_SHOW)
        time.sleep(1)