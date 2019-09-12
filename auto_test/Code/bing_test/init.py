from selenium import webdriver
import unittest


class Init(unittest.TestCase):
    def setUp(self):
        self.url = 'https://cn.bing.com'
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        self.driver.get(self.url)

    # 结束测试固件
    def tearDown(self):
        self.driver.quit()


