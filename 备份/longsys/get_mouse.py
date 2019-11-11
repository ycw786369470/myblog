import pyautogui
import time

if __name__ == '__main__':
    while 1:
        x, y = pyautogui.position()
        print(f'x坐标:{x},y坐标:{y}')
        time.sleep(1.5)
