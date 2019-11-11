import pyperclip
import pyautogui
from pywinauto.application import Application
import os
import time as t
import csv


"""
    由于HDTune写入测试必须先清除磁盘分区，将该测试的顺序放在首位。
    ### 必须打包并以管理员身份运行 ###
    1、手动清除磁盘信息（删除分区等）
    2、开始写、读测试
    3、完成后保存log并分析
    4、初始化磁盘添加卷(需要借助CDI的操作磁盘)
"""
class HDTune(object):
    def __init__(self):
        # 外部main函数用
        os.environ.update({"__COMPAT_LAYER": "RUnAsInvoker"})
        self.path = os.path.abspath('.')
        self.img_path = self.path + '\HDTune\img\\'
        self.txt_path = self.path + '\HDTune\\txt\\'
        self.rep_path = self.path + '\HDTune\\rep\\'
        self.testing = None
        self.localtime = t.strftime('%Y-%m-%d-%H-%M-%S', t.localtime(t.time()))
        self.cdi_btn_path = 'D:\\tools\CDI\\btn\\'

    def hdt_open(self):
        Application(backend='uia').start(r'D:\tools\HDTune\HDTune.exe')
        t.sleep(1)

    def cdi_open(self):
        Application(backend='uia').start(r'D:\tools\CDI\DiskInfo64.exe')
        t.sleep(1)

    def hdt_settings(self):
        # 点击 '文件'
        pyautogui.moveTo(653, 270)
        pyautogui.click()
        t.sleep(0.5)
        for i in range(2):
            pyautogui.press('up')
        pyautogui.press('enter')
        # 选择基准
        pyautogui.press('down')
        pyautogui.moveTo(867, 390)
        pyautogui.click()
        t.sleep(0.5)
        pyautogui.click(850, 510)
        for i in range(4):
            pyautogui.press('down')
        pyautogui.press('enter')
        # 选择磁盘
        pyautogui.moveTo(735, 297)
        t.sleep(0.5)
        for i in range(3):
            pyautogui.press('down')

    def hdt_settings_test(self):
        # 点击 '文件'
        pyautogui.moveTo(653, 270)
        pyautogui.click()
        t.sleep(0.5)
        for i in range(2):
            pyautogui.press('up')
        pyautogui.press('enter')
        # 选择基准
        pyautogui.press('down')
        pyautogui.click(850, 510)
        for i in range(4):
            pyautogui.press('up')
        pyautogui.press('enter')
        # 选择磁盘
        pyautogui.moveTo(735, 297)
        t.sleep(0.5)
        for i in range(3):
            pyautogui.press('down')

    def hdt_write(self):
        self.testing = 'write'
        # 选择写入
        write_pos = pyautogui.locateOnScreen(r'D:\tools\HDTune\btn\write.png')
        if write_pos:
            x, y = pyautogui.center(write_pos)
            pyautogui.click(x, y)
        else:
            print('查找‘写入’失去焦点')
            x, y = 1175, 458
            pyautogui.click(x, y)
        # 点击开始
        start_pos = pyautogui.locateOnScreen(r'D:\tools\HDTune\btn\start.png')
        if start_pos:
            x, y = pyautogui.center(start_pos)
            pyautogui.click(x, y)
        else:
            print('查找‘开始’按钮失去焦点')
            x, y = 1210, 390
            pyautogui.click(x, y)
        # 勾选确认以及开始
        choose_pos = pyautogui.locateOnScreen(r'D:\tools\HDTune\btn\choose.png')
        if choose_pos:
            x, y = pyautogui.center(choose_pos)
            pyautogui.click(x, y)
        else:
            print('查找‘勾选框’失去焦点')
            x, y = 950, 555
            pyautogui.click(x, y)
        t.sleep(0.1)
        pyautogui.press('enter')

    def hdt_read(self):
        self.testing = 'read'
        # 选择读取
        read_pos = pyautogui.locateOnScreen(r'D:\tools\HDTune\btn\read.png')
        if read_pos:
            x, y = pyautogui.center(read_pos)
            pyautogui.click(x, y)
        else:
            print('查找‘读取’失去焦点')
            x, y = 1182, 436
            pyautogui.click(x, y)
        # 点击开始
        start_pos = pyautogui.locateOnScreen(r'D:\tools\HDTune\btn\start.png')
        if start_pos:
            x, y = pyautogui.center(start_pos)
            pyautogui.click(x, y)
        else:
            print('查找‘开始’按钮失去焦点')
            x, y = 1210, 390
            pyautogui.click(x, y)

    # 等待前一项测试结束
    def hdt_wait(self):
        pyautogui.moveTo(925, 240, duration=0.5, tween=pyautogui.easeInOutQuad)
        while 1:
            start_pos = pyautogui.locateOnScreen(r'D:\tools\HDTune\btn\start.png')
            if start_pos:
                self.hdt_screen_shot(self.testing)
                self.hdt_save_txt(self.testing)
                break
            else:
                print('测试中...')

    def hdt_screen_shot(self, method):
        print(f'{method}测试完成,正在生成截图...')
        img_path = os.path.join(self.img_path, f'{method}-{self.localtime}.png')
        pyautogui.screenshot(img_path, region=(620, 225, 680, 585))
        print(f'生成{method}测试截图完成！')

    # 保存日志文件
    def hdt_save_txt(self, method):
        txt_name = f'{method}-{self.localtime}.txt'
        txt_path = os.path.join(self.txt_path, txt_name)
        rep_name = f'{method}-{self.localtime}.csv'
        rep_path = os.path.join(self.rep_path, rep_name)
        pyautogui.moveTo(653, 270)
        pyautogui.click()
        pyautogui.press('down')
        pyautogui.press('enter')
        data = pyperclip.paste()
        with open(txt_path, 'w', encoding='gbk') as ft:
            ft.write(data)
            print(f'{txt_name}写入完成！')
        data = data.replace('\r', '').split('\n')[5: -1]
        with open(rep_path, 'w+') as fr:
            writer = csv.writer(fr)
            for d in data:
                writer.writerow(d.split(':'))
        print('生成rep完成')

    def hdt_close(self):
        t.sleep(0.5)
        pyautogui.click(1270, 240)

    def cdi_open_disk(self):
        t.sleep(0.5)
        pyautogui.moveTo(755, 138)
        pyautogui.click()
        for i in range(2):
            pyautogui.press('up')
        pyautogui.press('enter')
        t.sleep(5)

    # 寻找未分配磁盘的位置并准备新建卷
    def cdi_find_disk(self):
        name_ls = ['un.png', 'un2.png']
        for i in name_ls:
            root = self.cdi_btn_path + i
            print(root)
            disk_pos = pyautogui.locateOnScreen(root)
            if disk_pos:
                x, y = pyautogui.center(disk_pos)
                pyautogui.rightClick(x, y)
                pyautogui.press('down')
                pyautogui.press('enter')
                break
            else:
                continue

    def cdi_new_disk(self):
        pyautogui.moveRel(100, 0)
        t.sleep(0.5)
        for i in range(5):
            pyautogui.press('enter')
            t.sleep(0.5)
        # 等待完成
        while 1:
            format_pos = pyautogui.locateOnScreen(self.cdi_btn_path + 'format.png')
            if format_pos:
                print('创建磁盘中...')
            else:
                print('创建磁盘成功！')
                break


def main():
    hdt = HDTune()
    hdt.hdt_open()
    # hdt.hdt_settings()
    hdt.hdt_settings_test()
    hdt.hdt_write()
    hdt.hdt_wait()
    hdt.hdt_read()
    hdt.hdt_wait()
    hdt.hdt_close()
    hdt.cdi_open()
    hdt.cdi_open_disk()
    hdt.cdi_find_disk()
    hdt.cdi_new_disk()


