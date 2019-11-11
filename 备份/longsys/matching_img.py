import pyautogui
from PIL import Image
import timeit


def to_position(file_name2):
    # 系统找图速率做对比
    res = pyautogui.locateCenterOnScreen(file_name2)


def get_position(file_name1, file_name2):
    im1 = Image.open(file_name1)    # 大图
    im2 = Image.open(file_name2)    # 查找的图
    pix1 = im1.load()
    pix2 = im2.load()
    width1 = im1.size[0]
    height1 = im1.size[1]
    width2 = im2.size[0]
    height2 = im2.size[1]

    rgb2 = pix2[0, 0][:3]  # 左上角起始点
    for x in range(width1):
        for y in range(height1):
            # print(x, y)
            rgb1 = pix1[x, y][:3]
            if rgb1 == rgb2:
                # 判断剩下的点是否相同
                status = 0
                # 图二的坐标是(s, j) --- (s-x, j-y)
                for s in range(x, x + width2 - 1):
                    for j in range(y, y + height2 - 1):
                        # 设置阈值范围
                        print(s-x, j-y)
                        if abs(pix2[s-x, j-y][0]-pix1[s, j][0]) > 60 and abs(
                               pix2[s-x, j-y][1]-pix1[s, j][1]) > 60 and abs(
                               pix2[s-x, j-y][2]-pix1[s, j][2]) > 60:
                            status = 1
                if status:
                    continue
                else:
                    return x + round(0.5 * width2), y + round(0.5 * height2)

if __name__ == '__main__':
    find_img = r'D:\tools\CDM6.0.0\btn\4k.png'
    big_img = r'D:\tools\CDM6.0.0\btn\exe.png'
    ret = get_position(big_img, find_img)
    print(ret)
