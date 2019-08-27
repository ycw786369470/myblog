from selenium import webdriver
import time
import json
import random


class HuyaSpider(object):
    def __init__(self):
        self.url = 'https://www.huya.com/g/lol'
        self.driver = webdriver.Chrome()

    def goto_web(self):
        self.driver.get(self.url)

    def get_data(self):
        n = 0
        li = self.driver.find_elements_by_xpath('//ul/li[@class="game-live-item"]')
        for i in li:
            name = i.find_element_by_xpath('.//span/span/i').get_attribute('title')
            title = i.find_element_by_xpath('.//a[2]').get_attribute('title')
            num = i.find_element_by_xpath('.//i[@class="js-num"]').text
            huya.save_data(name, title, num)

    def next_page(self):
        try:
            self.driver.find_element_by_class_name('laypage_next').click()
        except:
            print('全部爬取完毕')

    def save_data(self, name, title, num):
        dict_data = {'主播:': name, '标题': title, '热度': num}
        # 将字典数据转换成json数据
        json_data = json.dumps(dict_data, ensure_ascii=False)
        with open('../txt/huya.txt'.format(i), 'a', encoding='utf-8') as f:
            f.write(json_data)
            f.write('\n')


if __name__ == '__main__':
    huya = HuyaSpider()
    huya.goto_web()
    for i in range(4):
        time.sleep(random.randint(2, 5))
        # 接收数据并保存
        huya.get_data()
        print('第{}页爬取完毕！'.format(i+1))
        # 尝试点击下一页
        huya.next_page()