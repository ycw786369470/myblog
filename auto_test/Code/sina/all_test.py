import os
import unittest
import HTMLTestRunner
import time


# 获取所有的测试模块
def all_cases():
    suite = unittest.TestLoader().discover(
        start_dir=os.path.join(os.path.dirname(__file__), 'test'),
        pattern='test_*.py',
        top_level_dir=None
    )
    return suite


def get_now_time():
    return time.strftime('%Y-%m-%d %H-%M-%S', time.localtime())


def run():
    filename = os.path.join(os.path.dirname(__file__), 'report', get_now_time() + 'repost.html')
    fp = open(filename, 'wb')
    runner = HTMLTestRunner.HTMLTestRunner(
        stream=fp,
        title='自动化测试',
        description='详情'
    )
    runner.run(all_cases())


if __name__ == '__main__':
    run()


