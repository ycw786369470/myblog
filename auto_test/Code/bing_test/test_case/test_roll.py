from ..init import *
import unittest
from selenium.webdriver.common.action_chains import ActionChains


class RollTest(Init):
    def test_input(self):
        search = self.driver.find_element_by_id("sb_form_q")
        # 测试是否可编辑
        self.assertTrue(search.is_enabled())

    def test_title(self):
        title = self.driver.title
        self.assertEqual(title, "微软 Bing 搜索 - 国内版")

    def test_seek(self):
        element = self.driver.find_element_by_id('sb_form_go')
        ActionChains(self.driver).move_to_element(element).perform()
        self.driver.save_screenshot("s.png")

    def test_search(self):
        self.driver.find_element_by_id("bs_from_q").send_keys("世界杯")
        self.driver.find_element_by_id("sb_form_go").click()
        self.assertEqual(self.driver.title, "世界杯 - 国内版 Bing")


if __name__ == '__main__':
    unittest.main(verbosity=2)