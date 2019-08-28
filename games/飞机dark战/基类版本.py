#飞机大战
#start_time:1_30
from pygame.locals import *
import pygame
from time import *

class BasePlane(object): # 飞机基类
    def __init__(self,screen_tmp,x,y,image_name):
        self.x = x
        self.y = y
        # 创建飞机模型
        self.p = pygame.image.load(image_name)
        self.screen = screen_tmp
        self.bullets = []

'''
    @Plane:飞机类初始化把屏幕导入,设定飞机初始位置
            $fire:飞机开火，将当时开火的位置传给self.bullets中，然后在disp中实现
            $disp:根据xy坐标显示飞机的位置以及打印子弹
            #move_:移动xy坐标改变飞机位置
'''
class Plane(BasePlane):
    def __init__(self,screen_tmp):
        BasePlane.__init__(self,screen_tmp,210,500,'.\图片\plane_2.png')

    # 飞机开火放进bullets中保存，也在disp中实现
    def fire(self): #
        self.bullets.append(Bullet(self.screen,self.x+20,self.y-10))

    def disp(self):
        # 显示飞机的模型＆位置
        self.screen.blit(self.p,(self.x,self.y))
        # 显示子弹的模型＆位置
        for bullet in self.bullets:
            bullet.disp()
            bullet.move()
            if bullet.y < 0:
                self.bullets.remove(bullet)

    def move_left(self):
        self.x -= 15

    def move_right(self):
        self.x += 15

    def move_up(self):
        self.y -= 15

    def move_down(self):
        self.y += 15

class Enemy(BasePlane):
    def __init__(self,screen_tmp):
        BasePlane.__init__(self,screen_tmp,0,0,'.\图片\Enimy_1.png')
        self.move_flag = 1
        self.time = 0

    # 飞机开火放进bullets中保存，也在disp中实现
    def fire(self): #
        self.bullets.append(EnimyBullet(self.screen,self.x+38,self.y + 40))

    def disp(self):
        # 显示飞机的模型＆位置
        self.screen.blit(self.p,(self.x,self.y))
        # 显示子弹的模型＆位置
        for bullet in self.bullets:
            bullet.disp()
            bullet.move()
            if bullet.y >= 700:
                self.bullets.remove(bullet)

    def move(self):
        if self.move_flag:
            self.x += 4
        else :
            self.x -= 4
        if self.x >= 400:
            self.time += 1
            self.move_flag = 0
        if self.x <= 0:
            self.time += 1
            self.move_flag = 1
        if self.x % 100 == 0:
            self.fire()
        #进入暴走模式！！！OFF
        if self.time >= 5:
            if self.x % 30 == 0: #修改此处可以选择难度
                self.fire()


'''
    @Bullets:子弹类，导入图片以及传入子弹坐标
        $disp:显示子弹
        $move:子弹上移
'''
class Bullet(object):
    def __init__(self,screen_tmp,x=0,y=0):
        self.x = x
        self.y = y # 飞机左边子弹
        self.x2 = x + 40 # 右边子弹
        self.screen = screen_tmp
        self.bul = pygame.image.load('.\图片\Bullet_2.png')

    def disp(self):
        self.screen.blit(self.bul,(self.x,self.y)) # 飞机左边的子弹
        self.screen.blit(self.bul,(self.x2,self.y)) # 飞机右边的子弹
        # print(self.x,self.y)

    def move(self):
        self.y -= 10 #子弹0.01s向上移动10像素

class EnimyBullet():
    def __init__(self,screen_tmp,x=0,y=0):
        self.x = x
        self.y = y
        self.screen = screen_tmp
        self.bul = pygame.image.load('.\图片\Gun_bullet.png')

    def disp(self):
        self.screen.blit(self.bul,(self.x,self.y)) # 飞机左边的子弹
        # print(self.x,self.y)

    def move(self):
        self.y += 10 #子弹每0.01s向上移动10像素


'''
    @Background类用于设置背景的导入和显示.
'''
class Background(object):
    def __init__(self,screen_tmp):
        self.bg = pygame.image.load('.\图片\Background.png')
        self.screen = screen_tmp
        self.x = 0
        self.y = 0
        self.flag_move = 1

    def disp(self): #显示背景
        self.screen.blit(self.bg, (self.x, self.y))

    def move(self):
        if self.flag_move == 1:
            self.x -= 1
        else:
            self.x += 1
        if self.x <= -200:
            self.flag_move = 0
        elif self.x >= 0:
            self.flag_move = 1
'''
    control根据监视键盘控制飞机移动
'''
def control(plane):
    for event in pygame.event.get():
        if event.type == QUIT:
            print('EXIT')
        elif event.type == KEYDOWN:
            if event.key == K_a or event.key == K_LEFT:
                plane.move_left()
            elif event.key == K_d or event.key == K_RIGHT:
                plane.move_right()
            elif event.key == K_w or event.key == K_UP:
                plane.move_up()
            elif event.key == K_s or event.key == K_DOWN:
                plane.move_down()
            elif event.key == K_SPACE:
                plane.fire()


def main1():
    #创建窗口 比例：bg:724 * 1200  plane:250 * 273
    s_pro = (500,700) #屏幕比例
    screen = pygame.display.set_mode(s_pro,0,32)
    bg = Background(screen)
    plane = Plane(screen)
    enimy = Enemy(screen)

    while 1:
        bg.disp() #在屏幕上显示背景和飞机的位置
        plane.disp() # 英雄飞机在最上层
        enimy.disp() #
        pygame.display.update()
        control(plane)
        enimy.move()
        bg.move()
        sleep(0.01)



if __name__ == '__main__':
    main1()
    # main2()


