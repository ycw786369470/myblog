import pyperclip
import pyautogui
from pywinauto.application import Application
import os
import time as t


'''
    H2testw1.4自动化测试步骤：
        0、格式化磁盘
        1、打开h2
        2、选择磁盘select target
        3、点击Write+Verify
        4、点击确认attention
        5、等待完成
        6、监听OK是否就绪，若已就绪则表示已完成
        7、在某个文件夹创建文件提取结果
        8、点击OK，结束
'''
class H2(object):
    def __init__(self):
        os.environ.update({"__COMPAT_LAYER": "RUnAsInvoker"})
        self.path = os.path.abspath('.')
        self.img_path = self.path + '\H2\img\\'

    def h2_open(self):
        app = Application(backend='uia').start(r'D:\tools\h2test\h2testw1.4\h2testw.exe')
        t.sleep(1)

    def select_disk(self):
        x, y = 1100, 475
        pyautogui.moveTo(x, y)
        pyautogui.click()
        t.sleep(0.5)
        # 上翻到最顶端
        for i in range(5):
            pyautogui.scroll(100)
        pyautogui.click(810, 415)
        # 检查是否已经展开‘此电脑’
        find = False
        opened_path = 'D:\\tools\h2test\\btn\opened\\'
        toopen_path = 'D:\\tools\h2test\\btn\\toopen\\'
        for f in os.listdir(opened_path):
            pos = pyautogui.locateOnScreen(opened_path + f)
            if pos is not None:
                find = True
                break
        if not find:
            print('正在打开此电脑')
            for f in os.listdir(toopen_path):
                pos = pyautogui.locateOnScreen(toopen_path + f)
                if pos is not None:
                    x, y = pyautogui.center(pos)
                    pyautogui.click(x, y)
                    break
        for i in range(4):
            pyautogui.scroll(-100)
        pyautogui.moveTo(990, 700)
        disks = pyautogui.locateAllOnScreen(r'D:\tools\h2test\btn\disk.png')
        disk = list(disks)[-1]
        x, y = pyautogui.center(disk)
        pyautogui.moveTo(x, y, duration=0.5, tween=pyautogui.easeInOutQuad)
        pyautogui.click()
        pyautogui.moveTo(990, 700, duration=0.5, tween=pyautogui.easeInOutQuad)
        pyautogui.click()

    def h2_start(self):
        x, y = 820, 625         # 指向write+verify
        pyautogui.click(x, y)
        x, y = 1130, 590        # 指向attention的OK
        pyautogui.click(x, y)

    # 测试模块，添加至程序中加快测试速度
    def h2_test_demo(self):
        pyautogui.click(781, 575)
        pyautogui.click(836, 575)
        pyautogui.typewrite('10')

    def h2_wait_over(self):
        ok_path = 'D:\\tools\h2test\\btn\ok\\'
        flag = True
        while flag:
            for i in os.listdir(ok_path):
                ret = pyautogui.locateOnScreen(ok_path + i)
                t.sleep(1)
                if ret is not None:
                    flag = False
                    print(i)
                    x, y = pyautogui.center(ret)
                    pyautogui.click(x, y)
                    break
            print('测试中...')

    def h2_close(self):
        x, y = 1144, 404
        pyautogui.moveTo(x, y, duration=1, tween=pyautogui.easeInOutQuad)
        pyautogui.click()
        print('已关闭')


def main():
    h2 = H2()
    h2.h2_open()
    h2.select_disk()
    # h2.h2_test_demo()
    h2.h2_start()
    h2.h2_wait_over()
    h2.h2_close()

if __name__ == '__main__':
    main()













