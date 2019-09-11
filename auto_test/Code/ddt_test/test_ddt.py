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

    @data(('', '', '请输入邮箱名'), ('', '123', '请输入邮箱名'), ('admin', '', '您输入的邮箱名格式不正确'))
    @unpack
    def test_login(self, uname, pword, result):
        self.driver.find_element_by_id('freename').send_keys(uname)
        self.driver.find_element_by_id('freepassword').send_keys(pword)
        self.driver.find_element_by_link_text('登录').click()
        # 查看错误提示
        res = self.driver.find_element_by_xpath('//div[@class="freeError"]/span[@class="loginError tip11"]').text
        self.assertEqual(result, res)
        time.sleep(3)


def get_data(index):
    with open(os.path.join(os.path.dirname(__file__), 'save.txt'), 'r', encoding='gbk') as f:
        d = f.readline()
    return d[index]


if __name__ == '__main__':
    s = unittest.main(verbosity=2)
    # get_data()
    











