import os
import unittest
import HTMLTestRunner
import time


def all_case():
    # 获取所有测试模块
    s = unittest.TestLoader().discover(
        # 获取当前文件路径
        start_dir=os.path.join(os.path.dirname(__file__), "test_case"),
        # 选择文件
        pattern="test_*.py",
        top_level_dir=None
    )
    return s


def get_now_time():
    return time.strftime('%Y-%m-%d %H-%M-%S', time.localtime())


def run():
    # 拼接文件路径
    file_name = os.path.join(
        os.path.dirname(__file__),
        "report",
        get_now_time() + '.html'
    ).replace('\\', '/')
    with open(file_name, "wb") as fp:
        runner = HTMLTestRunner.HTMLTestRunner(
            stream=fp,
            title="自动化测试",
            description="必应测试"
        )
        runner.run(all_case())


if __name__ == '__main__':
    run()





