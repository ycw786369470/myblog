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

    def test_sina_title(self):
        title = self.driver.title
        self.assertEqual(title, '新浪邮箱')
        self.driver.get(self.url)

    def test_sina_news(self):
        uname_box = self.driver.find_element_by_id('freename')
        pword_box = self.driver.find_element_by_id('freepassword')
        self.assertTrue(uname_box.is_enabled())
        self.assertTrue(pword_box.is_enabled())

    def test_sina_input(self):
        input_box = self.driver.find_element_by_id('store1')
        self.assertTrue(input_box.is_selected())


if __name__ == '__main__':
    unittest.main(verbosity=2)



