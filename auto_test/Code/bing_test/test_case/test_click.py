from Code.bing_test.init import *
import unittest
import time
from ddt import ddt, unpack, data


bing_data = [
    ["图片", "https://cn.bing.com/images/trending?form=Z9LH"],  # 图片
    ["视频", "https://cn.bing.com/videos/trending"],            # 视频
    ["学术", "https://cn.bing.com/academic?FORM=HDRSC4"]        # 学术
]


@ddt
class ClickTest(Init):
    # 测试图片点击
    @data(*bing_data)
    @unpack
    def test_click(self, to_web, result):
        self.driver.find_element_by_link_text(to_web).click()
        self.assertEqual(self.driver.current_url, result)
        time.sleep(3)


if __name__ == '__main__':
    unittest.main(verbosity=2)