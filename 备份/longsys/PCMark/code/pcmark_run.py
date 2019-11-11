import pyperclip
import pyautogui
from pywinauto.application import Application
import os
import time as t
from PCMark.code.pcmark_log import *

class PCMark(object):
    def __init__(self):
        os.environ.update({"__COMPAT_LAYER": "RUnAsInvoker"})
        # 外部main函数用
        self.path = os.path.abspath('.')
        self.img_path = self.path + '\PcMark\\img\\'
        self.log_path = self.path + '\PcMark\\log\\'
        self.rep_path = self.path + '\PcMark\\rep\\'

    def pcm_open(self):
        app = Application(backend='uia').start(r'C:\Program Files\Futuremark\PCMark 8\bin\PCMark8.exe')
        t.sleep(7)

    def pcm_help(self):
        help_pos = pyautogui.locateOnScreen(r'D:\tools\PcMark\btn\help.png')
        if help_pos:
            x, y = pyautogui.center(help_pos)
            pyautogui.moveTo(x, y)
            pyautogui.click()
        else:
            x, y = 1583, 177
            pyautogui.moveTo(x, y)
            pyautogui.click()
        # 辨别options第一项是否marked
        marked = pyautogui.locateOnScreen(r'D:\tools\PcMark\btn\marked.png')
        if marked:
            x, y = pyautogui.center(marked)
            pyautogui.moveTo(x, y)
            pyautogui.click()
        t.sleep(1)

    def pcm_start(self):
        benck = pyautogui.locateOnScreen(r'D:\tools\PcMark\btn\help.png')
        if benck:
            x, y = pyautogui.locateOnScreen(r'D:\tools\PcMark\btn\bench.png')
            pyautogui.moveTo(x, y)
            pyautogui.click()
        else:
            x, y = 1280, 178
            pyautogui.moveTo(x, y)
            pyautogui.click()
        # 选择测试SSD
        t.sleep(0.5)
        x, y = 1204, 350
        pyautogui.moveTo(x, y, duration=0.5, tween=pyautogui.easeInOutQuad)
        pyautogui.click()
        t.sleep(1)
        # 选择磁盘
        x, y = 1210, 567
        pyautogui.doubleClick(x, y)
        for i in range(5):
            pyautogui.press('down')
        t.sleep(0.5)
        # 点击run按钮
        run_pos = pyautogui.locateOnScreen(r'D:\tools\PcMark\btn\run.png')
        if run_pos:
            x, y = pyautogui.center(run_pos)
            pyautogui.moveTo(x, y)
            pyautogui.click()
        else:
            x, y = 1400, 780
            pyautogui.moveTo(x, y)
            pyautogui.click()

    def pcm_wait(self):
        while 1:
            export_pos = pyautogui.locateOnScreen(r'D:\tools\PcMark\btn\export.png')
            if export_pos:
                x, y = pyautogui.center(export_pos)
                t.sleep(0.5)
                print(x, y)
                pyautogui.moveTo(x, y, duration=0.5, tween=pyautogui.easeInOutQuad)
                pyautogui.doubleClick()
                t.sleep(0.5)
                print('测试完成！')
                break
            else:
                print('测试中...')
                t.sleep(3)

    def pcm_save_log(self):
        t.sleep(1)
        localtime = t.strftime('%Y-%m-%d-%H-%M-%S', t.localtime(t.time()))
        # 点击输入地址
        path = self.log_path
        pyperclip.copy(path)
        pyautogui.moveTo(850, 190, duration=0.5, tween=pyautogui.easeInOutQuad)
        pyautogui.click()
        pyautogui.hotkey('ctrl', 'v')
        pyautogui.press('enter')
        # 输入文件名
        pyautogui.moveTo(737, 585)
        pyautogui.click()
        log_name = f'log-{localtime}.xml'
        pyautogui.typewrite(log_name)
        # 点击保存
        x, y = 1080, 650
        pyautogui.moveTo(x, y, duration=0.5, tween=pyautogui.easeInOutQuad)
        pyautogui.click()
        t.sleep(0.5)
        pyautogui.press('space')
        t.sleep(0.5)
        # 截图
        img_path = os.path.join(self.img_path, f'img-{localtime}.png')
        pyautogui.screenshot(img_path, region=(285, 110, 1360, 850))
        print('保存log完毕,等待分析数据')
        return log_name

    def pcm_close(self):
        x, y = 1611, 127
        pyautogui.moveTo(x, y, duration=0.5, tween=pyautogui.easeInOutQuad)
        pyautogui.click()


def main():
    pcm = PCMark()
    pcm.pcm_open()
    pcm.pcm_help()
    pcm.pcm_start()
    pcm.pcm_help()
    pcm.pcm_wait()
    log_name = pcm.pcm_save_log()
    log = PcMarkLog(pcm.log_path, pcm.rep_path, log_name)
    log.data_clean()
    pcm.pcm_close()
