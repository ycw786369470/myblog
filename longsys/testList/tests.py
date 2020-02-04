# from django.test import TestCase
# import wmi
# c = wmi.WMI()
# last = 0
#
# # Create your tests here.
# for physical_disk in c.Win32_DiskDrive():
#     for partition in physical_disk.associators("Win32_DiskDriveToDiskPartition"):
#         for logical_disk in partition.associators("Win32_LogicalDiskToPartition"):
#             last = logical_disk.Caption[:1]
#
# print(last)

import xlrd
import os


def many_device():
    path = str(os.path.abspath('..'))
    file_name = path + '\static\device_manage\相机表.xlsx'
    start_row = 4  # 起始行
    # 获取数据
    data = xlrd.open_workbook(file_name.replace('\\', '/'))
    camera = []
    # sheet-1
    sheet1 = data.sheets()[0]
    nrows = sheet1.nrows
    print(nrows)
    # for i in range(start_row, nrows):
    #     camera.append(sheet1.row_values(i))
    #     print(sheet1.row_values(i))


many_device()
