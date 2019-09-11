from selenium import webdriver
import time
import unittest
from ddt import ddt, data, unpack
import os


@ddt
class SinaTest(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.url = 'https://mail.sina.com.cn/'
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        self.driver.get(self.url)

    # 结束测试固件
    @classmethod
    def tearDownClass(self):
        self.driver.quit()

    def login(self, uname, pword):
        self.driver.find_element_by_id('freename').send_keys(uname)
        self.driver.find_element_by_id('freepassword').send_keys(pword)
        self.driver.find_element_by_link_text('登录').click()

    def test_div(self):
        txt = self.driver.find_element_by_xpath('//div[@class="freeError"]/span[@class="loginError tip11"]').text
        return txt

    def test_uname_pword_null(self):
        self.login(get_data(0), get_data(0))
        self.assertEqual(self.test_div(), get_data(2))
        time.sleep(5)
        self.driver.get(self.url)

    def test_uname_null(self):
        self.login(get_data(0), get_data(1))
        self.assertEqual(self.test_div(), get_data(2))
        time.sleep(3)
        self.driver.get(self.url)

    def test_pword_null(self):
        self.login(get_data(1), get_data(0))
        self.assertEqual(self.test_div(), get_data(3))
        time.sleep(3)
        self.driver.get(self.url)


def get_data(index):
    with open(os.path.join(os.path.dirname(__file__), 'save.txt'), 'r', encoding='utf-8') as f:
        d = f.readlines()
        return d[index].replace('\n', '')


if __name__ == '__main__':
    s = unittest.main(verbosity=2)
    # get_data()












