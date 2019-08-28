# 王校长大作战！
# 规则：使用王校长在IG比赛现场食用的热狗攻击***
import pygame
import time
from pygame.locals import *
import random

pygame.init()
pygame.mixer.init()


'''
    @WXZ王校长类：
        王校长的属性:xy坐标,发射时和就绪状态的img以及热狗子弹的列表
        : wxz_display 用来显示王校长的图像
        : wxz_move 王校长的移动方式
            分为两个阶段:向上(正常、缓冲)、向下(正常、缓冲)
        :shoot 发射面包，通过control函数监控键盘按空格space来调用
'''
class WXZ(object):
    def __init__(self,screen_tmp): #初始化图片和坐标
        self.screen = screen_tmp
        self.x = 50
        self.y = 50
        self.music = pygame.mixer.Sound('./Music/shoot2.wav') # Sound用wav格式，否则报错！
        self.wxz_ready_img = './Image/ready_副本.png'
        self.wxz_shoot_img = './Image/shoot_副本.png'
        self.img = pygame.image.load(self.wxz_ready_img)
        self.move_flag = 1 # 用来控制上下移动的标志位，为1时下移，为0时上移
        self.shoot_list = [] #用来存放发射的热狗的数据

    def wxz_display(self):
        self.screen.blit(self.img,(self.x,self.y)) # 第一个参数为图片，第二个为坐标元组


    # 热狗的长:112，热狗的宽:70
    # 水果长宽100*100
    def wxz_hd(self,list_prey):
        for hotdog in self.shoot_list:
            hotdog.hd_display()
            hotdog.hd_move()
            #判断是否击中水果
            for prey in list_prey:
                #px、py为水果的原点坐标，pname是水果的名字
                px,py,pname = prey.x,prey.y,prey.name
                # 判断击中区域代码块，结合36行注释理解
                #================================================================#
                if px + 100 > hotdog.x + 112 > px and py + 100 > hotdog.y + 70 > py:
                    # print('{:}被热狗的右下角击中！'.format(pname))
                    self.shoot_list.remove(hotdog)  #撞到水果热狗移除
                    return prey # 击中则返回水果函数的的入口
                elif px + 100 > hotdog.x > px and py + 100 > hotdog.y + 70 > py:
                    # print('{:}被热狗的右下角击中！'.format(pname))
                    self.shoot_list.remove(hotdog)
                    return prey
                elif px + 100 > hotdog.x > px and py + 100 > hotdog.y > py:
                    # print('{:}被热狗的右下角击中！'.format(pname))
                    self.shoot_list.remove(hotdog)
                    return prey
                elif px + 100 > hotdog.x + 112 > px and py + 100 > hotdog.y + 70 > py:
                    # print('{:}被热狗的右下角击中！'.format(pname))
                    self.shoot_list.remove(hotdog)
                    return prey
                #================================================================#
            #越界处理：当热狗飞出屏幕之外。
            if hotdog.x > 1000 or hotdog.y > 500 :
                self.shoot_list.remove(hotdog)

    # 人物上下移动的时候，在顶端或者下端会出现缓冲动作
    def wxz_move(self):
        top = 0 #上方起点
        bottom = 350 #下方终点
        px = 5 #每次移动的距离
        gap_t = self.y - top
        gap_b = bottom - self.y

        if self.move_flag:
            # 当距离底端70px 开始缓冲过程
            if gap_b <= 70:
                if gap_b <= 30:
                    if gap_b <= 10:
                        self.y += 1
                    else:
                        self.y += 2
                else:
                    self.y += 4
            # 缓冲结束
            else:
                self.y += px
            if self.y == bottom: #到达底端标志位通知往上走
                self.move_flag = 0

        elif self.move_flag == 0: #缓冲见上方
            if gap_t <= 70:
                if gap_t <= 30:
                    if gap_t <= 10:
                        self.y -= 1
                    else:
                        self.y -= 2
                else:
                    self.y -= 4
            else:
                self.y -= px
            if self.y == top:  # 到达顶端
                self.move_flag = 1

    def shoot(self):
        self.shoot_list.append(McHotdog(self.screen,self.x + 105,self.y + 25)) # +为矫正发射热狗的位置
        self.music.play( )


'''
    @Prey类:是怪物元素的基类
        有自己的x、y轴坐标
        运动方式: 从屏幕下抛起来，有一个合适的-y轴初速度，+y轴的一个加速度
'''
class Prey(object): # 猎物的类
    def __init__(self, screen_tmp, img, name, x, y = 500): # 默认y初始值为500，因为是从底部上来
        self.name = name
        self.x = x
        self.y = y
        self.screen = screen_tmp
        self.init_y = random.randint(15,22) # 默认的向上初始速度,随机数增加随机性
        self.acc = -0.5 # 默认的初始加速度（↓）
        self.img = pygame.image.load(img) # 加载水果图片

    def prey_display(self):
        self.screen.blit(self.img, (self.x, self.y))

    def prey_move(self):
        self.y -= self.init_y  #水果的初速度
        self.init_y += self.acc #水果落地的加速度

    def prey_boom(self):
        pass

class Apple(Prey):
    def __init__(self, sceen_tmp, x):
        Prey.__init__(self, sceen_tmp, './Image/apple.png', '苹果', x)

class Watermelon(Prey):
    def __init__(self, sceen_tmp, x):
        Prey.__init__(self, sceen_tmp, './Image/wt.png', '西瓜', x)

class Orange(Prey):
    def __init__(self, sceen_tmp, x):
        Prey.__init__(self, sceen_tmp, './Image/orange.png', '橘子', x)

class Kiwi(Prey):
    def __init__(self, sceen_tmp, x):
        Prey.__init__(self, sceen_tmp, './Image/kiwi.png', '猕猴桃', x)

class Pea(Prey):
    def __init__(self, sceen_tmp, x):
        Prey.__init__(self, sceen_tmp, './Image/pea.png', '梨', x)

class Lemon(Prey):
    def __init__(self, sceen_tmp, x):
        Prey.__init__(self, sceen_tmp, './Image/lemon.png', '柠檬', x)

class Paw(Prey):
    def __init__(self, sceen_tmp, x):
        Prey.__init__(self, sceen_tmp, './Image/paw.png', '木瓜', x)



'''
    @McHotdog类：定义热狗的图像、坐标等
        运动方式:
            有一个x轴横向速度，在y轴纵向有一个初始速度为0,和一个合适的加速度
            使其看起来更符(tuo)合(li)物理逻辑
'''
class McHotdog(object):
    def __init__(self,screen_tmp,x,y):
        self.x = x
        self.y = y
        self.screen = screen_tmp
        self.hd_img = pygame.image.load('./Image/hotdog.png')
        self.init_vx = 20
        self.init_vy = 0 # 初始y轴速度
        self.acc = 0.75 # y轴加速度

    def hd_display(self):
        self.screen.blit(self.hd_img,(self.x,self.y))

    def hd_move(self):
        self.x += self.init_vx
        self.y += self.init_vy
        self.init_vy += self.acc

'''
    @BG类：就是存放背景万达广场，没了
'''

class BG(object):
    def __init__(self,screen_tmp):
        self.screen = screen_tmp
        self.x = 0
        self.y = 0
        self.img = pygame.image.load('./Image/vanda2.jpg')
        self.info = pygame.image.load('./Image/interf2.png')
    def bg_display(self):
        self.screen.blit(self.img, (self.x, self.y)) # 第一个参数为图片，第二个为坐标元组
        self.screen.blit(self.info, (self.x+750, self.y + 10)) # 第一个参数为图片，第二个为坐标元组


class Info(object):
    def __init__(self,screen_tmp):
        self.screen = screen_tmp
        self.x = 0
        self.y = 0
        self.img = pygame.image.load('./Image/vanda2.jpg')
        self.info = pygame.image.load('./Image/interf2.png')
        self.button_start = pygame.image.load('./Image/button_play.png')

    # button的长为300px高为100
    def info_display(self):
        self.screen.blit(self.img, (self.x, self.y)) # 第一个参数为图片，第二个为坐标元组
        self.screen.blit(self.info, (self.x+750, self.y + 10)) # 第一个参数为图片，第二个为坐标元组
        self.screen.blit(self.button_start, (350, 110)) #开始按钮的位置

'''
    控制王校长吞吐热狗~
'''
def control(wxz):
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                wxz.shoot()

def choose_start(info):
    choosing = True
    while choosing:
        info.info_display()
        pygame.display.update()
        time.sleep(0.01)
        for event in pygame.event.get():
            # if event.type == MOUSEMOTION: #即时鼠标位置
            #     mouse_x, mouse_y = event.pos
            #     move_x, move_y = event.rel
            #     print(mouse_x,mouse_y,move_x,move_y)
            #=========================================测试结束
            if event.type == MOUSEBUTTONDOWN:
                # mouse_down = event.button   #点击的时候返回1
                mouse_x, mouse_y = event.pos  #返回点击坐标
                # print(mouse_x,mouse_y)
                if 370 < mouse_x < 630 and 200 < mouse_y < 300:
                    # print('start')
                    choosing = False

def easy():
    score = 0  # 记录玩家的得分
    # rec_px = 0  # 记录王校长总共移动的px
    s_pro = (1000, 500)  # 默认纵横比例为500px:1000px
    screen = pygame.display.set_mode(s_pro, 0, 32)  # 初始化屏幕
    bg = BG(screen)
    wxz = WXZ(screen)
    list_prey = [Apple, Watermelon, Orange, Kiwi, Lemon, Pea, Paw]  # 保存在列表里方便调用
    list_ready = [] # 就绪的水果
    flag_prey = 1
    info = Info(screen) #实例化初始页面
    #   进入开始界面
    choose_start(info)
    is_start = True
    while is_start:
        list_pxy = []  # 保存prey的当前x/y位置，给热狗来判断是否命中
        # rec_px += 5
        bg.bg_display()  # 显示背景
        wxz.wxz_display()  # 显示王校长的位置
        wxz.wxz_move()  # 王校长上下移动
        control(wxz)  # 按空格控制王校长发射热狗
        if flag_prey:
            x = random.randint(300, 900)
            index_prey = random.randint(0, len(list_prey) - 1)
            list_ready.append(list_prey[index_prey](screen, x))
            if len(list_ready) >= 4:  # 设置最多N个水果同时存在
                flag_prey = 0
        for i in list_ready:
            list_pxy.append(i)
            i.prey_display()
            i.prey_move()
            if i.y > 500:
                list_ready.remove(i)
            if len(list_ready) < 2:  # 当场上水果少于N个继续增加
                flag_prey = 1
        lost_prey = wxz.wxz_hd(list_pxy)  # 返回被打中的prey的函数入口
        if lost_prey is not None:
            list_ready.remove(lost_prey)
            score += 1
            print('当前得分:{:}~'.format(score))
        pygame.display.update()
        time.sleep(0.01)

def middle():
    score = 0  # 记录玩家的得分
    rec_px = 0  # 记录王校长总共移动的px
    s_pro = (1000, 500)  # 默认纵横比例为500px:1000px
    screen = pygame.display.set_mode(s_pro, 0, 32)  # 初始化屏幕
    bg = BG(screen)
    wxz = WXZ(screen)
    list_prey = [Apple, Watermelon, Orange, Kiwi, Lemon, Pea, Paw]  # 保存在列表里方便调用
    list_ready = []
    flag_prey = 1

    while 1:
        list_pxy = []  # 保存prey的当前x/y位置，给热狗来判断是否命中
        rec_px += 5
        bg.bg_display()  # 显示背景
        wxz.wxz_display()  # 显示王校长的位置
        wxz.wxz_move()  # 王校长上下移动
        control(wxz)  # 按空格控制王校长发射热狗
        if flag_prey:
            x = random.randint(300, 900)
            index_prey = random.randint(0, len(list_prey) - 1)
            list_ready.append(list_prey[index_prey](screen, x))
            if len(list_ready) >= 10:  # 设置最多N个水果同时存在
                flag_prey = 0
        for i in list_ready:
            list_pxy.append(i)
            i.prey_display()
            i.prey_move()
            if i.y > 500:
                list_ready.remove(i)
            if len(list_ready) < 2:  # 当场上水果少于N个继续增加
                flag_prey = 1
        lost_prey = wxz.wxz_hd(list_pxy)  # 返回被打中的prey的函数入口
        if lost_prey is not None:
            list_ready.remove(lost_prey)
            score += 1
            print('当前得分:{:}~'.format(score))
        pygame.display.update()
        time.sleep(0.01)

if __name__ == '__main__':
    easy()
