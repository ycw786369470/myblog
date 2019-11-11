import csv
import os
from CDM.code.check_perf import *


class CdmWrite(object):
    def __init__(self, log_filename, path, ver):
        self.path = path
        if ver == 600:
            ver = 'x6_0_0\\'
        elif ver == 512:
            ver = 'x5_1_2\\'
        self.log_path = os.path.join(self.path + '\CDM\log\\' + ver)
        self.report_path = os.path.join(self.path + '\CDM\\rep\\' + ver)
        self.log_path = '{}{}'.format(self.log_path, log_filename)
        self.report_filename = log_filename.split('.')[0].replace('log', 'rep')
        self.report_filename = f'{self.report_filename}.csv'
        self.report_path = '{}{}'.format(self.report_path, self.report_filename)

    #读取生成的txt日志文件数据
    def read_data(self,ver):
        self.write_header()
        with open(self.log_path, 'r', encoding='utf-16le', newline='') as file:
            for line in file:
                line = line.strip()
                try:
                    if line[0] == 'S' or line[0] == 'R':
                        data_list = line.split(':')
                        #将封装好的数据写入csv文件中
                        # print(data_list)
                        self.write_data(data_list)
                except:
                    pass
        print('写入csv!')
        #写入校验结果
        cop = Compare(self.report_path)
        if ver == 600:
            cop.comp_600()
        if ver == 512:
            cop.comp_512()

    def write_header(self):
        with open(self.report_path, 'a+', encoding='utf-8', newline='') as f:
            headers = ['Testing', 'Speed']
            writer = csv.writer(f)
            writer.writerow(headers)

    #写入csv
    def write_data(self, data_list):
        rows = [(data_list[0], data_list[1].strip(' ')[0:6])]
        with open(self.report_path, 'a+', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(rows)



