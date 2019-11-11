import shutil
import os
import psutil


###!!!  清除最后一个磁盘的内容（一定要在插u盘时使用）  !!!###
def get_root():
    disks_num = str(len(psutil.disk_partitions()))
    # 通过ASCII🐎关系由磁盘数量获取最后一个磁盘(插入盘)
    disk = chr(ord(disks_num) + 18)
    root = f"{disk}:\\"
    return root


def main():
    root = get_root()
    for f in os.listdir(root):
        file_path = os.path.join(root, f)
        if os.path.isfile(file_path):
            # 防误删
            if f[-3:] == 'h2w' or f[-3:] == 'tst':
                os.remove(file_path)
                print(file_path + '已删除')
        elif os.path.isdir(file_path):
            if f[0: 3] == 'PCM':
                shutil.rmtree(file_path, True)
                print('dir ' + file_path + '已删除')
    print(root + '盘格式化完成！')