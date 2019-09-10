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

    # 测试用例
    def test_baidu_news(self):
        self.driver.find_element_by_link_text('新闻').click()
        self.driver.get(self.url)

    def test_baidu_map(self):
        self.driver.find_element_by_link_text('地图').click()
        self.driver.get(self.url)


if __name__ == '__main__':
    # 顺序测试
    suite = unittest.TestSuite()
    suite.addTest(BaiduTest("test_baidu_map"))
    suite.addTest(BaiduTest("test_baidu_news"))
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
    # 无序测试
    # unittest.main(verbosity=2)


