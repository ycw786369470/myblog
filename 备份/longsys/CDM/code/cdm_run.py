'''
    CrystalDiskMark 5.1.2/6.0.0/7.0.0(beta) 
    自动化测试步骤：
        0、格式化磁盘
        1、实例化对象auto
        2、cdm_open()方法打开cdm程序
        3、自动化选择测试次数
        4、点击all按钮开始测试,监听测试完成
        5、测试完毕后截图、保存log文件
            (1)截图文件格式：地址：CDM/img/x版本号/img-年-月-日-时-分.png
            (2)txt文件格式：地址：CDM/log/x版本号/log-年-月-日-时-分.txt
        6、提取txt数据，生成csv文件CDM/rep/x版本号/rep-年-月-日-时-分.csv
    异常处理:
        1、磁盘空间已满（通过每项测试开始前格式化解决√）
        2、偶尔打不开cdm软件（延时解决√）
        3、关于all图标不同机器找不到（通过调整分辨率或者更新截图解决√）
        4、每台机器分辨率不同的问题
'''
import pyperclip
import pyautogui
from pywinauto.application import Application
import os
import time as t
from CDM.code import cdm_log


class CDM(object):
    def __init__(self):
        os.environ.update({"__COMPAT_LAYER": "RUnAsInvoker"})
        self.path = os.path.abspath('.')     # '.'为当前目录  '..'为父级目录
        self.ver = 0
        self.img_path = ''
        self.log_path = ''
        self.btn_all = (800, 410)

    def cdm_open_512(self):
        self.ver = 512
        app = Application(backend='uia').start(r'D:\tools\CDM5.1.2\DiskMark64.exe')
        self.img_path = self.path + '\CDM\img\\x5_1_2\\'
        self.log_path = self.path + '\CDM\log\\x5_1_2\\'
        t.sleep(1)

    def cdm_open_600(self):
        self.ver = 600
        app = Application(backend='uia').start(r'D:\tools\CDM6.0.0\CrystalDiskMark.exe')
        self.img_path = self.path + '\CDM\img\\x6_0_0\\'
        self.log_path = self.path + '\CDM\log\\x6_0_0\\'
        t.sleep(1)

    def cdm_700_run(self):
        self.ver = 700
        app = Application(backend='uia').start(r'D:\tools\CDM7.0.0\DiskMark64.exe')
        self.img_path = self.path + '\CDM\img\\x7_0_0\\'
        self.log_path = self.path + '\CDM\log\\x7_0_0\\'
        # 调节次数
        pyautogui.moveTo(820, 410)
        pyautogui.scroll(10)

    # 截图
    def screen_shot(self):
        localtime = t.strftime('%Y-%m-%d-%H-%M-%S', t.localtime(t.time()))
        root = f''
        x, y = 760, 335
        width = 400
        height = 370
        root = f'{self.img_path}{localtime}.png'
        img1 = pyautogui.screenshot(root, region=(x, y, width, height))
        print('截图成功!' + root)

    # 跳转至文件
    def cdm_2_files(self):
        x, y = 780, 370
        pyautogui.moveTo(x, y)
        pyautogui.click()

    # 跳转至all按钮
    def cdm_2_all_512(self):
        flag = False
        x, y = self.btn_all
        path = 'D:\\tools\CDM5.1.2\\btn\\'
        for f in os.listdir(path):
            pos_box = pyautogui.locateOnScreen(path + f)
            if pos_box is not None:
                x, y = pyautogui.center(pos_box)
                pyautogui.moveTo(x, y, duration=0.5, tween=pyautogui.easeInOutQuad)
                pyautogui.click()
                flag = True
                break
        if flag is False:
            pyautogui.moveTo(x, y, duration=0.5, tween=pyautogui.easeInOutQuad)
            pyautogui.click()
        t.sleep(0.5)

    def cdm_2_all_600(self):
        flag = False
        x, y = self.btn_all
        path = 'D:\\tools\CDM6.0.0\\btn\\'
        for f in os.listdir(path):
            pos_box = pyautogui.locateOnScreen(path + f)
            if pos_box is not None:
                x, y = pyautogui.center(pos_box)
                pyautogui.moveTo(x, y, duration=0.5, tween=pyautogui.easeInOutQuad)
                pyautogui.click()
                flag = True
                break
        if flag is False:
            pyautogui.moveTo(x, y, duration=0.5, tween=pyautogui.easeInOutQuad)
            pyautogui.click()
        t.sleep(0.5)

    # 跳转至空闲区(用在点击开始按钮后)
    def cdm_2_empty(self):
        x, y = 930, 350
        pyautogui.moveTo(x, y, duration=0.5, tween=pyautogui.easeInOutQuad)

    def cdm_wait(self):
        flag = 1
        pos_box = 0
        while flag:
            if self.ver == 600:
                path = 'D:\\tools\CDM6.0.0\\btn\\'
                for f in os.listdir(path):
                    pos_box = pyautogui.locateOnScreen(path + f)
            elif self.ver == 512:
                path = 'D:\\tools\CDM5.1.2\\btn\\'
                for btn in os.listdir(path):
                    pos_box = pyautogui.locateOnScreen(path + btn)
            print('测试已完成' if pos_box else '测试中...')
            if pos_box is None:
                t.sleep(2)
                continue
            else:
                flag = 0

    def cdm_save_txt(self):
        self.log_path = self.log_path
        localtime = t.strftime('%Y-%m-%d-%H-%M-%S', t.localtime(t.time()))
        log_name = f'log-{localtime}.txt'
        self.cdm_2_files()
        x, y = 810, 415
        pyautogui.moveTo(x, y)
        pyautogui.click()
        x1, y1 = 970, 280   # 输入地址坐标
        pyautogui.moveTo(x1, y1, duration=0.5, tween=pyautogui.easeInOutQuad)
        pyautogui.click()
        pyperclip.copy(self.log_path)
        pyautogui.hotkey('ctrl', 'v')
        pyautogui.press('enter')
        x2, y2 = 970, 670   # 输入文件名坐标
        pyautogui.moveTo(x2, y2)
        pyautogui.click()
        pyperclip.copy(log_name)
        pyautogui.hotkey('ctrl', 'v')
        x3, y3 = 1410, 740  # 保存按钮坐标
        pyautogui.moveTo(x3, y3)
        pyautogui.click()
        print('保存完毕!' + self.log_path)
        return log_name

    def cdm_choose_time(self):
        if self.ver == 600:
            x, x1 = 855, 855
            y, y1 = 400, 335
            pyautogui.moveTo(x, y)
            pyautogui.click()
            pyautogui.moveTo(x1, y1)
            pyautogui.click()
        elif self.ver == 512:
            x, y = 855, 400
            pyautogui.moveTo(x, y)
            pyautogui.doubleClick()
            for i in range(8):
                pyautogui.scroll(5)
            pyautogui.press('enter')

    # 选择测试盘
    def cdm_choose_disk(self):
        # print('选择磁盘')
        if self.ver == 600:
            x, y = 1040, 410
            pyautogui.moveTo(x, y)
            pyautogui.doubleClick()
            pyautogui.press('esc')
            t.sleep(0.5)
            for i in range(5):
                pyautogui.scroll(-10)
            pyautogui.press('esc')
            pyautogui.scroll(10)
            t.sleep(0.5)
        elif self.ver == 512:
            for i in range(2):
                pyautogui.press('tab')
            for i in range(4):
                pyautogui.press('down')
                pyautogui.press('esc')
            pyautogui.press('up')

    # 关闭CDM窗口
    def cdm_close(self):
        x, y = 1140, 350
        pyautogui.moveTo(x, y, duration=0.5, tween=pyautogui.easeInOutQuad)
        pyautogui.click()


def cdm_6_0_0():
    start_time = t.time()
    auto = CDM()
    auto.cdm_open_600()
    auto.cdm_choose_time()
    auto.cdm_choose_disk()
    auto.cdm_2_all_600()
    auto.cdm_2_empty()
    auto.cdm_wait()
    # 测试完成
    auto.screen_shot()
    log_filename = auto.cdm_save_txt()
    auto.cdm_close()
    log = cdm_log.CdmWrite(log_filename, auto.path, auto.ver)
    log.read_data(auto.ver)
    end_time = t.time()
    all_time = end_time - start_time
    print(all_time)


def cdm_5_1_2():
    start_time = t.time()
    auto = CDM()
    auto.cdm_open_512()
    auto.cdm_choose_time()
    auto.cdm_choose_disk()
    auto.cdm_2_all_512()
    auto.cdm_2_empty()
    auto.cdm_wait()
    # 测试完成
    auto.screen_shot()
    log_filename = auto.cdm_save_txt()
    auto.cdm_close()
    t.sleep(2)
    log = cdm_log.CdmWrite(log_filename, auto.path, auto.ver)
    log.read_data(auto.ver)
    end_time = t.time()
    all_time = end_time - start_time
    print(all_time)


def cdm_7_0_0():
    auto = CDM()
    auto.cdm_700_run()


def cdm():
    print('开始测试6.0.0版本')
    cdm_6_0_0()
    t.sleep(1)
    print('开始测试5.1.2版本')
    cdm_5_1_2()
