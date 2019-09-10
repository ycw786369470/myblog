import unittest
from selenium import webdriver


class BaiduTest(unittest.TestCase):
    # 开始测试固件
    @classmethod
    def setUpClass(self):
        self.url = 'https://www.baidu.com/'
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.implicitly_wait(5)
        self.driver.get(self.url)

    # 结束测试固件
    @classmethod
    def tearDownClass(self):
        self.driver.quit()