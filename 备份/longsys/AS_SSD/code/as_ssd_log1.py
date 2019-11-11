from bs4 import BeautifulSoup
import xml
import os


class AsSsdLog(object):
    def __init__(self, log_path, log_name):
        self.path = os.path.abspath('.')
        self.log_path = log_path
        self.log_name = log_name
        self.rep_path = os.path.join(self.path + '\AS_SSD\\rep\\')

    def data_clean(self):
        print('提取日志文件关键字段...')
        print(self.log_path + self.log_name)
        with open(self.log_path + self.log_name, 'r', encoding='utf-8') as f:
            r = f.read()
        bs = BeautifulSoup(r, 'xml')
        # 顺序读写
        seqTest = bs.find('SeqTest')
        seq_Read = seqTest.find('Read').text
        seq_Write = seqTest.find('Write').text
        # 4k 1队列随机读写
        Random4K1TTest = bs.find('Random4K1TTest')
        R_4K1T_Read = Random4K1TTest.find('Read').text
        R_4K1T_Write = Random4K1TTest.find('Write').text
        # 4k 64队列随机读写
        Random4K64TTest = bs.find('Random4K64TTest')
        R_4K64T_Read = Random4K64TTest.find('Read').text
        R_4K64T_Write = Random4K64TTest.find('Write').text

        AccTimeTest = bs.find('AccTimeTest')
        AccTime_Read = AccTimeTest.find('Read').text
        AccTime_Write = AccTimeTest.find('Write').text

        data_dict = {}
        data_dict['seq_Read'] = seq_Read
        data_dict['seq_Write'] = seq_Write
        data_dict['R_4K1T_Read'] = R_4K1T_Read
        data_dict['R_4K1T_Write'] = R_4K1T_Write
        data_dict['R_4K64T_Read'] = R_4K64T_Read
        data_dict['R_4K64T_Write'] = R_4K64T_Write
        data_dict['AccTime_Read'] = AccTime_Read
        data_dict['AccTime_Write'] = AccTime_Write

        self.write_data(data_dict)
        print('提取完毕...')

    def write_data(self, data_dict):
        rep_name = self.log_name.replace('xml', 'txt')
        rep_path = os.path.join(self.rep_path + rep_name)
        with open(rep_path, 'a+', encoding='utf-8') as f:
            for data in data_dict:
                f.write(data+':'+data_dict[data]+'\n')


