import os

#  在测试开始前检测是否文件夹齐全，会自动补足缺少的文件夹
def check():
    path = os.path.abspath('..')
    img_path = os.path.join(path, 'img')
    rep_path = os.path.join(path, 'rep')
    log_path = os.path.join(path, 'log')
    if not os.path.exists(img_path):
        os.mkdir(img_path)
    if not os.path.exists(rep_path):
        os.mkdir(rep_path)
    if not os.path.exists(log_path):
        os.mkdir(log_path)