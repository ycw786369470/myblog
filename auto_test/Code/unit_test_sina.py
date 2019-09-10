import unittest
from selenium import webdriver


class SinaTest(unittest.TestCase):
    # 开始测试固件
    @classmethod
    def setUpClass(self):
        self.url = 'https://mail.sina.com.cn/'
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.implicitly_wait(8)
        self.driver.get(self.url)

    # 结束测试固件
    @classmethod
    def tearDownClass(self):
        self.driver.quit()

    def test_sina_news(self):
        self.driver.find_element_by_id('freename').send_keys('123')
        self.driver.find_element_by_id('freepassword').send_keys('123')
        self.driver.find_element_by_link_text('登录').click()


if __name__ == '__main__':
    unittest.main(verbosity=2)



