from .sperate_firm import *


class Test(BaiduTest):
    # 测试用例
    def test_baidu_news(self):
        self.driver.find_element_by_link_text('新闻').click()
        self.driver.get(self.url)

    def test_baidu_map(self):
        self.driver.find_element_by_link_text('地图').click()
        self.driver.get(self.url)


if __name__ == '__main__':
    unittest.main(verbosity=2)