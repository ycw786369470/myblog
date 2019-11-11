import pyperclip
import pyautogui
from pywinauto.application import Application
import os
import time as t
from IOmeter.code.iometer_log import *

class IoMeter(object):
    def __init__(self):
        os.environ.update({"__COMPAT_LAYER": "RUnAsInvoker"})
        self.path = os.path.abspath('.')  # '.'为当前目录  '..'为父级目录
        self.img_path = ''
        self.log_path = ''
        self.localtime = t.strftime('%Y-%m-%d-%H-%M-%S', t.localtime(t.time()))

    def iometer_open(self):
        app = Application(backend='uia').start(r'D:\tools\IOMeter\IOmeter.exe')
        self.log_path_10G = os.path.join(self.path + '\IOmeter\log_10G\\')
        self.log_path_0 = os.path.join(self.path + '\IOmeter\log_0\\')
        t.sleep(0.5)

    #加载配置文件
    def load_icf(self,filename):
        print('加载配置文件...')
        load_btn = pyautogui.locateOnScreen(r'D:\tools\IOMeter\btn\load_btn.png')
        x, y = pyautogui.center(load_btn)
        pyautogui.moveTo(x, y, duration=0.5, tween=pyautogui.easeInOutQuad)
        pyautogui.click()
        t.sleep(1)
        #选择配置文件
        pyperclip.copy(filename)
        file_x, file_y = x + 435 ,y + 235
        pyautogui.moveTo(file_x, file_y, duration=0.5, tween=pyautogui.easeInOutQuad)
        pyautogui.click()
        pyautogui.hotkey('ctrl','v')
        pyautogui.press('enter')
        return x,y

    #选择磁盘
    def choose_disk(self,x,y):
        print('选择磁盘...')
        #点击加号
        add_x = x + 25
        add_y = y + 85
        pyautogui.moveTo(add_x, add_y, duration=0.5, tween=pyautogui.easeInOutQuad)
        pyautogui.click()
        #选择磁盘
        worker_x = x + 90
        worker_y = y + 100
        pyautogui.moveTo(worker_x, worker_y, duration=0.5, tween=pyautogui.easeInOutQuad)
        pyautogui.click()
        disk_x = x + 230
        disk_y = y + 95
        pyautogui.moveTo(disk_x, disk_y, duration=0.5, tween=pyautogui.easeInOutQuad)
        pyautogui.click()

        #选择最后一个磁盘
        for i in range(6):
            pyautogui.press('down')

    #开始测试
    def iometer_start(self):
        start_btn = pyautogui.locateOnScreen(r'D:\tools\IOMeter\btn\start_btn.png')
        x, y = pyautogui.center(start_btn)
        pyautogui.moveTo(x, y, duration=0.5, tween=pyautogui.easeInOutQuad)
        pyautogui.click()

    #保存日志文件
    def save_log(self,size):
        print('保存日志文件...')
        if size == 10:
            log_name = 'log_10G-{}.csv'.format(self.localtime)
        else:
            log_name = 'log_0-{}.csv'.format(self.localtime)
        start_btn = pyautogui.locateOnScreen(r'D:\tools\IOMeter\btn\save_results.png')
        if start_btn:
            x, y = pyautogui.center(start_btn)
            path_x, path_y = x + 530, y + 30
            pyautogui.moveTo(path_x, path_y, duration=0.5, tween=pyautogui.easeInOutQuad)
            pyautogui.click()
        else:
            x, y = 1110, 380
            pyautogui.click()

        if size == 10:
            pyperclip.copy(self.log_path_10G)
            pyautogui.hotkey('ctrl','v')
            pyautogui.press('enter')
        else:
            pyperclip.copy(self.log_path_0)
            pyautogui.hotkey('ctrl', 'v')
            pyautogui.press('enter')
        # 输入文件名坐标
        file_x,file_y = 960 , 770
        pyautogui.moveTo(file_x, file_y, duration=0.5, tween=pyautogui.easeInOutQuad)
        pyautogui.click()
        pyautogui.hotkey('ctrl','a')
        pyperclip.copy(log_name)
        pyautogui.hotkey('ctrl','v')
        #保存
        pyautogui.press('enter')
        return log_name

    #检测是否测试完成
    def end_check(self):
        flag = 1
        while flag:
            end_img = pyautogui.locateOnScreen(r'D:\tools\IOMeter\btn\start_btn.png')
            if end_img:
                print('测试完成！')
                break
            else:
                print('IOmeter测试中...')
                t.sleep(2)
                continue

    #关闭测试工具
    def iometer_close(self,x,y):
        close_x , close_y = x + 810 , y - 40
        pyautogui.moveTo(close_x, close_y, duration=0.5, tween=pyautogui.easeInOutQuad)
        pyautogui.click()


#SATA_10G测试
def iometer_10G():
    size = 10
    IM = IoMeter()
    IM.iometer_open()
    filename = r'iometer-10G.icf'
    x, y = IM.load_icf(filename)
    IM.choose_disk(x, y)
    IM.iometer_start()
    t.sleep(1)
    log_name = IM.save_log(size)
    IM.end_check()
    IM.iometer_close(x,y)
    #提取数据
    rep_path = os.path.join(IM.path+ '\IOmeter\\rep\\SATA_10G\\')
    IMLog = IoMeterLog(IM.log_path_10G,log_name,rep_path)
    data_dict = IMLog.data_clean()
    IMLog.write_rep(data_dict)


#SATA_满盘测试
def iometer_0():
    size = 0
    IM = IoMeter()
    IM.iometer_open()
    filename = r'iometer-0.icf'
    x, y = IM.load_icf(filename)
    IM.choose_disk(x, y)
    IM.iometer_start()
    t.sleep(1)
    log_name = IM.save_log(size)
    IM.end_check()
    IM.iometer_close(x,y)
    # 提取数据
    rep_path = os.path.join(IM.path + '\IOmeter\\rep\\SATA_0\\')
    IMLog = IoMeterLog(IM.log_path_0, log_name, rep_path)
    data_dict = IMLog.data_clean()
    IMLog.write_rep(data_dict)