import pyperclip
import pyautogui
from pywinauto.application import Application
import os
import time as t
import psutil
import csv


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
    异常处理：
        选择被测磁盘异常(通过修改ini初始化文件选择√)
'''
class H2(object):
    def __init__(self):
        os.environ.update({"__COMPAT_LAYER": "RUnAsInvoker"})
        # 外部main函数用
        self.path = os.path.abspath('.')
        self.img_path = self.path + '\H2\img\\'
        self.txt_path = self.path + '\H2\\txt\\'
        self.rep_path = self.path + '\H2\\rep\\'
        # 本文件使用
        # self.path = os.path.abspath('..')
        # self.img_path = self.path + '\img\\'
        # self.txt_path = self.path + '\\txt\\'
        # self.rep_path = self.path + '\\rep\\'

    def h2_open(self):
        app = Application(backend='uia').start(r'D:\tools\h2test\h2testw1.4\h2testw.exe')
        t.sleep(0.5)

    def select_disk(self):
        disks_num = str(len(psutil.disk_partitions()))
        # 通过ASCII🐎关系由磁盘数量获取最后一个磁盘
        disk = chr(ord(disks_num) + 18)
        with open(r'D:\tools\h2test\h2testw1.4\h2testw.ini', 'w') as h2:
            h2.write(f'[default]\nPath={disk}:\\')
            print('写入完毕！')

    def h2_start(self):
        x, y = 820, 625         # 指向write+verify
        pyautogui.click(x, y)
        t.sleep(0.5)
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
            print('测试中...')
            for i in os.listdir(ok_path):
                ret = pyautogui.locateOnScreen(ok_path + i)
                t.sleep(1)
                if ret:
                    flag = False
                    x, y = pyautogui.center(ret)
                    pyautogui.click(850, 655)
                    t.sleep(0.5)
                    pyautogui.click(x, y)
                    break

    def save_txt(self):
        data = pyperclip.paste()
        localtime = t.strftime('%Y-%m-%d-%H-%M-%S', t.localtime(t.time()))
        self.txt_name = f'txt-{localtime}.txt'
        self.rep_name = f'txt-{localtime}.csv'
        with open(self.txt_path + self.txt_name, 'w') as f:
            f.write(data)
            print('txt保存完毕')

    def h2_close(self):
        x, y = 1144, 404
        pyautogui.moveTo(x, y)
        pyautogui.click()
        t.sleep(0.5)

    def h2_rep(self):
        rep_ls = []
        with open(self.txt_path + self.txt_name, 'r+') as f:
            for i in range(0, 10):
                txt = f.readline()
                if i == 6 or i == 8:
                    rep_ls.append(txt.replace('\n', '').split(':'))
        with open(self.rep_path + self.rep_name, 'w+') as f:
            headers = ['Testing', 'Speed']
            writer = csv.writer(f)
            writer.writerow(headers)
            for data in rep_ls:
                writer.writerow(data)
            print('生成rep完成！')


def main():
    h2 = H2()
    h2.h2_open()
    h2.select_disk()
    h2.h2_test_demo()
    h2.h2_start()
    h2.h2_wait_over()
    h2.save_txt()
    h2.h2_close()
    h2.h2_rep()














