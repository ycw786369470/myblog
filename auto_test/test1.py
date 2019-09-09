from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait


class AutoTest(object):
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.url = 'https://www.baidu.com/'
        self.username = ''
        self.password = ''
        # 判断是否需要重新获取cookies，如果要获取则会在go_web方法时进行保存
        # 获取的cookies存放到page_cookie文件夹下
        # with open('page_cookie.txt', 'r', encoding='utf-8') as c:
        #     if len(c.read()) == 0:
        #         # 如果cookies为空则需要登录
        #         self.need_get_cookies = True
        #     else:
        #         self.need_get_cookies = False

    def go_web(self):
        self.driver.get(self.url)
        self.driver.maximize_window()
        # 判断是否需要登录
        # if self.need_get_cookies is True:
        #     self.login()
        #     # cookies = self.driver.get_cookies()
        # else:
        #     pass

    def login(self):
        pass

    def get_data(self):
        print(self.driver.title)

    def find_news(self):
        self.driver.find_element_by_link_text('新闻').click()

    def quit_driver(self):
        self.driver.quit()

    # 前进一页
    def forward_page(self):
        self.driver.forward()

    # 回退一页
    def back_page(self):
        self.driver.back()

    # 获取窗口句柄
    def get_handle(self):
        # 获取当前的窗口句柄
        now_handle = self.driver.current_window_handle
        # 获取所有窗口句柄
        handles = self.driver.window_handles
        print(now_handle)
        # print(handles)

    # 判断是否可见,可见返回True,不可见返回False
    def is_disp(self):
        self.driver.find_element_by_link_text('目标').is_displayed()

    # 判断是否能编辑
    def is_edit(self):
        self.driver.find_element_by_link_text('目标').is_enabled()

    # 判断是否已选中
    def is_sele(self):
        self.driver.find_element_by_link_text('目标').is_selected()

    # 下拉框
    def select_set(self):
        setting = self.driver.find_element_by_link_text('设置')
        # 下拉框操作，鼠标移至下拉框上
        ActionChains(self.driver).move_to_element(setting).perform()
        # 点击设置中的‘搜索设置’
        self.driver.find_element_by_link_text('搜索设置').click()
        time.sleep(2)
        # 实例化一个下拉框
        nr = self.driver.find_element_by_id('nr')
        select_find_num = Select(nr)
        # 可根据索引和下拉框选择
        select_find_num.select_by_index(1)
        # select_find_num.select_by_value(50)
        self.driver.find_element_by_class_name('prefpanelgo').click()
        # 转移到弹出框
        alert = self.driver.switch_to_alert()
        time.sleep(2)
        # 获取文本信息、点击确认
        print(alert.text)
        alert.accept()

    # 等待类——隐式、显式
    # 隐式等待implicitly_wait：设置最长的等待时间
    def wait_test(self):
        # 设置隐式等待时间为10s,10s之后还找不到就报错
        self.driver.implicitly_wait(10)
        self.driver.find_element_by_name('目标元素')


if __name__ == '__main__':
    auto = AutoTest()
    auto.go_web()
    # auto.alert()
    auto.select_set()
    # auto.find_news()
    # auto.get_data()
    # auto.get_handle()




