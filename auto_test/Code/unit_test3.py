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

    def test_baidu_search(self):
        so = self.driver.find_element_by_id('kw')
        # 断言判断是否通过，判断结果是否是True
        self.assertTrue(so.is_enabled())

    def test_baidu_title(self):
        title = self.driver.title
        # 断言判断title是否相同
        self.assertEqual(title, "百度一下")


if __name__ == '__main__':
    unittest.main(verbosity=2)



