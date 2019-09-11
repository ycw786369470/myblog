import unittest
from selenium import webdriver
from ddt import data, unpack, ddt
import csv


def getCsv(row, col):
    rows = []
    with open('input.csv') as f:
        reader = csv.reader(f)
        for iter in reader:
            rows.append(iter)
    return ''.join(rows[row][col])


class SinaLogin(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.implicitly_wait(30)
        self.driver.get('[图片]https://mail.sina.com.cn/#')

    def tearDown(self):
        self.driver.quit()

    def login(self, username, password):
        # 测试新浪邮箱登录N种情况
        self.driver.find_element_by_id('freename').send_keys(username)
        self.driver.find_element_by_id('freepassword').send_keys(password)
        self.driver.find_element_by_link_text('登录').click()

    def test_div(self):
        divTest = self.driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/div/div[4]/div[1]/div[1]/div[1]/span[1]').text
        return divTest

    def test_username_password_null(self):
        self.login(getCsv(0,0), getCsv(0,1))
        self.assertTrue(self.test_div(), getCsv(0,2))

    def test_username_null(self):
        self.login(getCsv(1,0), getCsv(1,1))
        self.assertTrue(self.test_div(), getCsv(1,2))

    def test_username_false(self):
        self.login(getCsv(2,0), getCsv(2,1))
        self.assertTrue(self.test_div(), getCsv(2,2))


if __name__ == '__main__':
    unittest.main(verbosity=2)
