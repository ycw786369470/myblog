from selenium import webdriver
import requests
from lxml import etree
import json
import time

class Dazhong(object):
    def __init__(self):
        # self.city_name = city_name
        # 存放所有url
        self.ls_urls = []
        self.url = 'https://hotels.ctrip.com/hotel/nanjing12#ctm_ref=hod_hp_sb_lst'
        # 初始化浏览器
        self.chrome = webdriver.Chrome()
        self.chrome.get(self.url)

    def find_city(self):
        # city_name = input('请输入您想查找的城市>>>')
        city_name = '长沙'
        # 模拟输入城市
        self.chrome.find_element_by_id('txtCity').send_keys(city_name)
        # 模拟点击搜索
        self.chrome.find_element_by_id('btnSearch').click()

    def next_page(self):
        time.sleep(2)
        self.chrome.find_element_by_id('downHerf').click()

    def run(self):
        hotel_name = self.chrome.find_elements_by_xpath('//h2[@class="hotel_name"]/a')
        for i in hotel_name:
            print(i.text)



if __name__ == '__main__':
    # name = input('输入城市名字>>>')
    dazhong = Dazhong()
    dazhong.run()
