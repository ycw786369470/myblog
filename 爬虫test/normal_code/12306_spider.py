from selenium import webdriver
import json
from selenium.webdriver.common.keys import Keys     # 引用selenium键盘模块
import time

class Page12306(object):
    def __init__(self):
        self.url = 'https://kyfw.12306.cn/otn/leftTicket/init?linktypeid=dc'
        self.driver = webdriver.Chrome()

    # 进入12306
    def goto_web(self):
        self.driver.get(self.url)
        self.driver.maximize_window()

    # 查找目的地
    def search_train(self):
        # 输入起点
        start_city = '长沙'
        # start_city = input('输入您的出发地>>>')
        # 输入目的地
        end_city = '武汉'
        # end_city = input('输入您的目的地>>>')
        # 找到两个输入框先清除再输入,并且找出查询按钮
        start_input = self.driver.find_element_by_id('fromStationText')
        end_input = self.driver.find_element_by_id('toStationText')
        search_btn = self.driver.find_element_by_id('query_ticket')
        # 填入起点
        # 针对12306反爬还得再获取一遍下拉列表元素
        start_input.click()
        start_input.clear()
        start_input.send_keys(start_city)
        start_input.send_keys(Keys.ENTER)
        time.sleep(1)
        # 填入终点
        end_input.click()
        end_input.clear()
        end_input.send_keys(end_city)
        end_input.send_keys(Keys.ENTER)
        # 模拟点击查询按钮
        search_btn.click()
        time.sleep(1)

    # 提取数据
    def get_data(self):
        print('进入提取数据')
        # train_nums = self.driver.find_elements_by_xpath('//div[@class="train"]//a')
        # for num in train_nums:
        #     print(num.text)
        # 获取出发和到达时间
        # all_time = self.driver.find_elements_by_xpath('//div[@class="cds"]')
        # for time in all_time:
        #     start_time = time.find_element_by_xpath('.//strong[1]').text
        #     end_time = time.find_element_by_xpath('.//strong[2]').text
        #     print('出发时间:{}/到达时间:{}'.format(start_time, end_time))
        # 历时
        history = self.driver.find_elements_by_xpath('//div[@class="ticket-info clearfix"]/div[4]')
        print(history)
        for i in history:
            time = i.find_element_by_xpath('.//strong').text
            print(time)

    # 存储数据
    def save_data(self, name, title, hot):
        pass


if __name__ == '__main__':
    page = Page12306()
    # 前往12306主页面
    page.goto_web()
    # 输入出发地、目的地查询车票
    page.search_train()
    # 取得车票数据
    page.get_data()
