#飞机大战
#start_time:1_30
from pygame.locals import *
import pygame
from time import *

'''
    @Plane:飞机类初始化把屏幕导入,设定飞机初始位置
            $fire:飞机开火，将当时开火的位置传给self.bullets中，然后在disp中实现
            $disp:根据xy坐标显示飞机的位置以及打印子弹
            #move_:移动xy坐标改变飞机位置
'''
class Game(object):
    def __init__(self,screen_tmp):
        self.screen = screen_tmp
        self.gameover_1 = pygame.image.load('.\图片\Gameover_1.png')
        self.gameover_2 = pygame.image.load('.\图片\Gameover_2.png')
        self.flag = 1
        self.num = 0

    def game_start(self):
        self.sleep_time = 0.5
        print('打飞机！启动！')
        sleep(self.sleep_time)
        # print('请选择难度\n1.一般\t2.测试难度\t3.喵喵喵???就一架敌机???')
        # choice = int(input('在此输入难度>>>'))
        print('选择难度完毕，加载游戏')
        sleep(self.sleep_time)
        print('Loading...')
        sleep(self.sleep_time)
        print('Loading....')
        sleep(self.sleep_time)
        print('Loading.....')
        sleep(self.sleep_time)
        print('游戏即将开始！')

    def game_over1(self):
        self.screen.blit(self.gameover_1,(100,50))

    def game_over2(self):
        self.screen.blit(self.gameover_2,(100,50))

class BasePlane(object):
    def __init__(self,screen_tmp,x,y,image_name):
        self.x = x
        self.y = y
        # 创建飞机模型
        self.p = pygame.image.load(image_name)
        self.screen = screen_tmp
        self.bullets = []

    def remove(self):
        self.x = 10000
        self.y = 10000

class Plane(BasePlane):
    def __init__(self,screen_tmp):
        BasePlane.__init__(self,screen_tmp,210,500,'.\图片\plane_2.png')

    # 飞机开火放进bullets中保存，在disp中实现
    def fire(self): #
        self.bullets.append(Bullet(self.screen,self.x+20,self.y-10))

    def disp(self,crash,enimy_xy): #同时在此步骤内加上检测是否击中敌机
        # 显示飞机的模型＆位置
        self.screen.blit(self.p,(self.x,self.y))
        # 显示子弹的模型＆位置
        for bullet in self.bullets:
            bullet.disp()
            bullet.move()
            if bullet.y < 0:
                self.bullets.remove(bullet)
            self.b_xy = (bullet.x,bullet.y)
            ret = crash.kill_enimies(self.b_xy,enimy_xy)
            if ret == 1:
                return 1

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

    def disp(self,crash,plane_xy):
        # 显示飞机的模型＆位置
        self.screen.blit(self.p,(self.x,self.y))
        # 显示子弹的模型＆位置
        for bullet in self.bullets:
            bullet.disp()
            bullet.move()
            if bullet.y >= 700:
                self.bullets.remove(bullet)
            self.b_xy = (bullet.x,bullet.y)
            ret = crash.be_kill(self.b_xy,plane_xy) #传入参数:敌人子弹坐标、英雄飞机的坐标
            if ret == 1:
                return 1

    def move(self):
        if self.move_flag and self.time % 2 == 0:
            self.x += 4
            self.y += 4
        elif self.move_flag == 0 :
            self.x -= 4
            self.y -= 4
        if self.x >= 400:
            self.time += 1
            self.move_flag = 0
        if self.x <= 0:
            self.time += 1
            self.move_flag = 1
        if self.x % 100 == 0:
            self.fire()
        #进入暴走模式！！！OFF
        if self.time >= 4:
            if self.x % 30 == 0: #修改此处可以选择难度
                self.fire()

'''
    @Bullet:子弹类，导入图片以及传入子弹坐标
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


# 检测碰撞类,目前默认敌我的大小为92*100，
# 己方子弹大小为14*50，敌方子弹大小为5*70
class Crash(object):
    def __init__(self,screen_tmp):
        self.screen = screen_tmp
        self.bullet = []
        self.enimy = []

    def boom(self,x,y):
        self.x = x - 30
        self.y = y - 30
        self.boom_shakalaka = pygame.image.load('.\图片\Boom.png')
        self.screen.blit(self.boom_shakalaka, (self.x, self.y)) # 在敌机坐标处爆炸


    # 检测攻击敌人,传入参数子弹的坐标以及敌人的坐标
    def kill_enimies(self,bullet,enimy):
        b_x,b_y = bullet
        e_x,e_y = enimy
        # 子弹（宽:b_x+14,长:b_y+50）
        # 如果子弹左上角坐标在飞机坐标方块范围内（宽:e_x+92,长:e_y+100）
        if b_x in range(e_x,e_x+92) and b_y in range(e_y,e_y+100):
            # print('1敌机被子弹左上击中了！')
            return 1
        # 如果子弹右上角坐标在飞机坐标方块范围内
        elif b_x+14 in range(e_x,e_x+92) and b_y in range(e_y,e_y+100):
            # print('2敌机被子弹右上击中了！')
            return 1
        # 如果子弹左下角坐标在飞机坐标方块范围内
        elif b_x in range(e_x,e_x+92) and b_y+50 in range(e_y,e_y+100):
            # print('3敌机被子弹左下击中了！')
            return 1
        # 如果子弹右下角坐标在飞机坐标范围内
        elif b_x+14 in range(e_x,e_x+92) and b_y+50 in range(e_y,e_y+100):
            # print('4敌机被子弹右下击中了！')
            return 1
    # 检测被攻击，传入敌人的子弹坐标以及自己的坐标


    def be_kill(self,e_bullet,plane): # 传入敌方子弹坐标和本机坐标
        e_x,e_y = e_bullet
        p_x,p_y = plane
        if e_x in range(p_x,p_x+92) and e_y in range(p_y,p_y+100):
            print('4右下被击中了！')
            return 1
        # 如果子弹右上角坐标在飞机坐标方块范围内
        elif e_x+5 in range(p_x,p_x+92) and e_y in range(p_y,p_y+100):
            print('4右下被击中了！')
            return 1
        # 如果子弹左下角坐标在飞机坐标方块范围内
        elif e_x in range(p_x,p_x+92) and e_y+70 in range(p_y,p_y+100):
            print('4右下被击中了！')
            return 1
        # 如果子弹右下角坐标在飞机坐标范围内
        elif e_x+5 in range(p_x,p_x+92) and e_y+70 in range(p_y,p_y+100):
            print('4右下被击中了！')
            return 1


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
            pass
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
    #===================================================
    #创建窗口 比例：bg:724 * 1200  plane:250 * 273
    s_pro = (500,700) #屏幕比例
    screen = pygame.display.set_mode(s_pro,0,32)
    game = Game(screen)
    bg = Background(screen)
    plane = Plane(screen)
    enimy = Enemy(screen)
    bullet = Bullet(screen)
    crash = Crash(screen)
    enimy_flag = 1  # 敌机的标识，为1时敌机正常移动，为0时标识敌机被击毁
    gameover_flag = 0
    game_time = 0
    plane_flag = 1 #英雄飞机的标志位，为0则表示被击中
    game.game_start() # 没用的
    #====================================================
    while 1:
        if game_time >= 400:
            game_time = 0
        game_time += 4
        pygame.display.update()
        bg.disp() #在屏幕上显示背景和飞机的位置

#=========================敌机被击中==================================#
        enimy_xy = (enimy.x, enimy.y)  # 敌机坐标
        ret_kill_enimy = plane.disp(crash,enimy_xy) # 显示飞机、传入敌机的坐标 若返回ret==1则表示敌机已被击中
        if ret_kill_enimy == 1:
            enimy_flag = 0 # 飞机停止移动
            crash.boom(enimy.x,enimy.y)
            enimy.remove()
            gameover_flag = 1
#===========================英雄被击中================================#
        plane_xy = (plane.x,plane.y)
        ret_be_kill = enimy.disp(crash,plane_xy) #显示敌机及子弹，包括判断是否击中英雄飞机
        if ret_be_kill == 1:
            plane_flag = 0
            crash.boom(plane.x,plane.y)
            plane.remove()
            gameover_flag = 1
#=====================================================================#
        if plane_flag:
            control(plane) # 如果plane_flag==1则可以控制飞机

        if enimy_flag:
            enimy.move()

        if gameover_flag == 1: #游戏是否结束
            if game_time >= 200:
                game.game_over1()
            else:
                game.game_over2()
        bg.move()

        sleep(0.01)

if __name__ == '__main__':
    main1()