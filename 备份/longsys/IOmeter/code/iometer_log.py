import csv
import os

class IoMeterLog(object):
    def __init__(self,log_path,log_name,rep_path):
        self.log_name = log_name
        self.log_path = os.path.join(log_path+self.log_name)
        self.rep_path = rep_path

    #数据清洗
    def data_clean(self):
        print('正在进行数据清洗...')
        data_dict = {}
        with open(self.log_path,encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                if row[0] == 'WORKER':
                    data_dict[row[2]] = row[6]
        print('清洗完成...')
        return data_dict

    def write_rep(self, data_dict):
        print('数据写入csv...')
        rep_name = self.log_name.replace('log', 'rep')
        rep_path = os.path.join(self.rep_path+rep_name)
        with open(rep_path,'a+',encoding='utf-8',newline='') as f:
            writer = csv.writer(f)
            for data in data_dict:
                row = [data,data_dict[data]]
                writer.writerow(row)
