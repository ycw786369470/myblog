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
        t.sleep(0.5)

    def select_disk(self):
        error = 0
        flag = True
        while flag:
            self.h2_open()
            # 鼠标移动到select
            x, y = 1100, 475
            pyautogui.moveTo(x, y)
            pyautogui.click()
            # 上翻到最顶端
            for i in range(5):
                pyautogui.scroll(100)
            pyautogui.click(900, 415)
            # try:
            net_pos = pyautogui.locateOnScreen('D:\\tools\h2test\\btn\disk.png')
            if net_pos:
                x, y = pyautogui.center(net_pos)
                pyautogui.moveTo(x, y)
                pyautogui.click()
                pyautogui.moveTo(990, 700)
                pyautogui.click()
                return error
            # except TypeError:
            else:
                error += 1
                pyautogui.press('esc')
                pyautogui.press('esc')
                continue

    def h2_start(self):
        x, y = 820, 625         # 指向write+verify
        pyautogui.click(x, y)
        x, y = 1130, 590        # 指向attention的OK
        pyautogui.click(x, y)

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
        pyautogui.moveTo(x, y)
        pyautogui.click()
        t.sleep(0.5)


def main():
    h2 = H2()
    e = 0
    all_times = 10
    test_times = 0
    while test_times < all_times:
        ret = h2.select_disk()
        if ret == 0:
            test_times += 1
        else:
            test_times += 1
            e += 1
        h2.h2_close()
        print(test_times)
    print('测试次数:' + str(all_times) + '错误数量:' + str(e))


if __name__ == '__main__':
    main()













