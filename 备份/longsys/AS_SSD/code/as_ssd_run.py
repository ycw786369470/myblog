'''
    安装bs4和lxml
'''
import pyperclip
import pyautogui
from pywinauto.application import Application
import os
import time as t
from AS_SSD.code.as_ssd_log import *


class AsSsd(object):
    def __init__(self):
        os.environ.update({"__COMPAT_LAYER": "RUnAsInvoker"})
        self.path = os.path.abspath('.')  # '.'为当前目录  '..'为父级目录
        self.img_path = os.path.join(self.path + '\AS_SSD\img\\')
        self.copy_img_path = os.path.join(self.path + '\AS_SSD\copy_img\\')
        self.log_path = os.path.join(self.path + '\AS_SSD\log\\')
        self.log_name = ''

    def as_ssd_open(self):
        app = Application(backend='uia').start(r'D:\tools\AS_SSD\AS SSD Benchmark.exe')
        t.sleep(3)

    # 匹配窗口的位置并选择磁盘
    def match_as_ssd(self):
        # 匹配窗口
        as_ssd_win = pyautogui.locateOnScreen(r'D:\tools\AS_SSD\btn\as_ssdwindow.png')
        t.sleep(1)
        x, y = pyautogui.center(as_ssd_win)
        # print(x,y)
        # 选择磁盘
        pyautogui.moveTo(x, y+50, duration=0.5, tween=pyautogui.easeInOutQuad)
        pyautogui.doubleClick()
        for i in range(6):
            pyautogui.press('down')
        return x, y

    # 跳转到start按钮
    def as_ssd_start(self):
        start = pyautogui.locateOnScreen(r'D:\tools\AS_SSD\btn\start.png')
        x, y = pyautogui.center(start)
        pyautogui.moveTo(x, y, duration=0.5, tween=pyautogui.easeInOutQuad)
        pyautogui.click()

    # 第一步测试的截图
    def first_screen_shot(self, x, y):
        localtime = t.strftime('%Y-%m-%d-%H-%M-%S', t.localtime(t.time()))
        pic_x = x - 115
        pic_y = y - 10
        width = 490
        height = 460
        root = '{}{}.png'.format(self.img_path, localtime)
        img1 = pyautogui.screenshot(root, region=(pic_x, pic_y, width, height))
        print('截图成功')

    # 保存日志文件
    def save_log(self, x, y):
        pyautogui.moveTo(x-105, y+30, duration=0.5, tween=pyautogui.easeInOutQuad)
        pyautogui.click()
        pyautogui.moveTo(x - 105, y + 70, duration=0.5, tween=pyautogui.easeInOutQuad)
        t.sleep(0.5)
        pyautogui.moveTo(x + 80, y + 70, duration=0.5, tween=pyautogui.easeInOutQuad)
        pyautogui.click()
        localtime = t.strftime('%Y-%m-%d-%H-%M-%S', t.localtime(t.time()))
        self.log_name = 'log-{}.xml'.format(localtime)
        # 输入保存路径
        pyautogui.moveTo(x + 530, y + 60, duration=0.5, tween=pyautogui.easeInOutQuad)
        pyautogui.click()
        pyperclip.copy(self.log_path)
        pyautogui.hotkey('ctrl', 'v')
        pyautogui.press('enter')
        # 输入文件名
        pyautogui.moveTo(x + 190, y + 450, duration=0.5, tween=pyautogui.easeInOutQuad)
        pyautogui.click()
        pyautogui.hotkey('ctrl', 'a')
        pyperclip.copy(self.log_name)
        pyautogui.hotkey('ctrl', 'v')
        pyautogui.moveTo(x + 670, y + 520, duration=0.5, tween=pyautogui.easeInOutQuad)
        pyautogui.click()

    # copy测试截图
    def copy_screen(self, x, y):
        localtime = t.strftime('%Y-%m-%d-%H-%M-%S', t.localtime(t.time()))
        pic_x = x - 8
        pic_y = y - 17
        width = 500
        height = 327
        root = '{}{}.png'.format(self.copy_img_path, localtime)
        img1 = pyautogui.screenshot(root, region=(pic_x, pic_y, width, height))
        print('截图成功')

    # 开始进行copy测试
    def copy_start(self, x, y):
        print('开始copy测试...')
        c_x = x + 35
        c_y = y + 25
        pyautogui.moveTo(c_x, c_y, duration=0.5, tween=pyautogui.easeInOutQuad)
        pyautogui.click()
        c_x_1 = c_x
        c_y_1 = c_y + 20
        pyautogui.moveTo(c_x_1, c_y_1, duration=0.5, tween=pyautogui.easeInOutQuad)
        pyautogui.click()
        # 匹配start按钮
        t.sleep(2)
        copy_win = pyautogui.locateOnScreen(r'D:\tools\AS_SSD\btn\copy_win3.PNG')
        t.sleep(1)
        w_x, w_y = pyautogui.center(copy_win)
        pyautogui.moveTo(w_x, w_y+290, duration=0.5, tween=pyautogui.easeInOutQuad)
        pyautogui.click()
        return w_x, w_y

    # 判断测试是否完成
    def end_check(self, img):
        flag = 1
        while flag:
            end_img = pyautogui.locateOnScreen(img)
            if end_img:
                print('测试完成！')
                break
            else:
                print('测试中...')
                pyautogui.press('space')
                t.sleep(5)
                continue

    # 关闭测试工具
    def as_ssd_close(self, x, y):
        pyautogui.moveTo(x + 365, y, duration=0.5, tween=pyautogui.easeInOutQuad)
        pyautogui.click()


def main():
    as_ssd = AsSsd()
    as_ssd.as_ssd_open()
    t.sleep(1)
    x, y = as_ssd.match_as_ssd()
    as_ssd.as_ssd_start()
    end_img = r'D:\tools\AS_SSD\btn\end_check.png'
    as_ssd.end_check(end_img)
    t.sleep(1)
    as_ssd.first_screen_shot(x, y)
    # 保存日志文件
    as_ssd.save_log(x, y)
    # 提取日志文件关键字段
    t.sleep(1)
    as_ssd_log = AsSsdLog(as_ssd.log_path, as_ssd.log_name)
    as_ssd_log.data_clean()
    t.sleep(1)
    w_x, w_y = as_ssd.copy_start(x, y)
    copy_end_img = r'D:\tools\AS_SSD\btn\copy_end_check.png'
    as_ssd.end_check(copy_end_img)
    # 保存copy测试截图
    as_ssd.copy_screen(w_y, w_y)
    as_ssd.as_ssd_close(x, y)
