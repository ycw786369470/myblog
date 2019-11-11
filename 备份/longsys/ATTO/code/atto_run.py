import pyautogui
from pywinauto.application import Application
import os
import time as t


class ATTO(object):
    def __init__(self):
        os.environ.update({"__COMPAT_LAYER": "RUnAsInvoker"})
        # 外部main函数用
        self.path = os.path.abspath('.')
        self.img_path = self.path + '\H2\img\\'
        # 本文件使用
        # self.path = os.path.abspath('..')
        # self.img_path = self.path + '\img\\'

    def atto_open(self):
        app = Application(backend='uia').start(r'D:\tools\ATTO\Bench32.exe')
        t.sleep(0.5)

    def atto_config(self):
        # 选择磁盘drive
        for i in range(4):
            pyautogui.press('down')
        # 选择Transfer size-from -4.0KB
        for i in range(2):
            pyautogui.press('tab')
        for i in range(5):
            pyautogui.keyDown('up')
        for i in range(3):
            pyautogui.press('down')
        # 选择Transfer size-to -1028.0KB
        pyautogui.press('tab')
        for i in range(15):
            pyautogui.keyDown('up')
        for i in range(11):
            pyautogui.press('down')
        pyautogui.press('tab')
        # 选择total length -128MB
        for i in range(15):
            pyautogui.keyDown('up')
        for i in range(11):
            pyautogui.press('down')
        # 点击start
        x, y = 1140, 425
        pyautogui.moveTo(x, y)
        pyautogui.click()

    # 等待测试完成并截图结果
    def atto_wait(self):
        t.sleep(10)
        btn_path = 'D:\\tools\ATTO\\btn\\wait.png'
        while 1:
            pos = pyautogui.locateOnScreen(btn_path)
            if pos:
                print('测试中...')
                t.sleep(3)
                continue
            else:
                print('测试完成！')
                break
        localtime = t.strftime('%Y-%m-%d-%H-%M-%S', t.localtime(t.time()))
        pyautogui.screenshot(
            os.path.join(
                self.img_path,
                f'img-{localtime}.png'
            ),
            region=(725, 210, 470, 610)
        )
        print('截图保存完毕！')

    def atto_close(self):
        x, y = 1170, 230
        pyautogui.click(x, y)
        pyautogui.press('right')
        pyautogui.press('enter')


def main():
    atto = ATTO()
    atto.atto_open()
    atto.atto_config()
    atto.atto_wait()
    atto.atto_close()
