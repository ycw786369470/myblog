from selenium import webdriver
import json
import time
import random


class DouyuSpider(object):
    def __init__(self):
        self.url = 'https://www.douyu.com/g_LOL'
        self.driver = webdriver.Chrome()
        self.page = 1

    # 进入斗鱼LOL主页
    def goto_web(self):
        self.driver.get(self.url)
        self.driver.maximize_window()

    # 提取数据
    def get_data(self):
        li_list = self.driver.find_elements_by_xpath('//ul[@class="layout-Cover-list"]/li')
        for li in li_list:
            title = li.find_element_by_xpath('.//div[@class="DyListCover-info"]/h3').text
            name = li.find_element_by_xpath('.//h2[@class="DyListCover-user"]').text
            hot = li.find_element_by_xpath('.//span[@class="DyListCover-hot"]').text
            self.save_data(name, title, hot)

    def next_page(self):
        self.page += 1
        self.driver.find_element_by_xpath('//input[@class="ListFooter-btn-input"]').clear()
        self.driver.find_element_by_xpath('//input[@class="ListFooter-btn-input"]').send_keys(self.page)
        self.driver.find_element_by_xpath('//span[@class="ListFooter-btn-label"]').click()

    def save_data(self, name, title, hot):
        dict_data = {'主播:': name, '标题:': title, '热度': hot}
        json_data = json.dumps(dict_data, ensure_ascii=False)
        with open('../txt/douyu.txt', 'a', encoding='utf-8') as f:
            f.write(json_data)
            f.write('\n')


if __name__ == '__main__':
    douyu = DouyuSpider()
    douyu.goto_web()
    for i in range(5):
        douyu.get_data()
        douyu.next_page()
        time.sleep(random.randint(3, 7))