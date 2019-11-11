import csv

class Compare(object):
    def __init__(self, report_path):
        self.seq_read = 500
        self.seq_write = 400
        self.random_4k_read = 200
        self.random_4k_write = 200
        self.report_path = report_path

    def comp_600(self):
        data_list = []
        with open(self.report_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for index, row in enumerate(reader):
                # 取出需要校验的数据与标准值进行比对
                # 校验顺序读取速度
                if index == 0:
                    self.check_func(data_list, row, self.seq_read)
                # 校验顺序写入速度
                if index == 1:
                    self.check_func(data_list, row, self.seq_write)

                # 校验4K随机读取速度
                if index == 4:
                    self.check_func(data_list, row, self.random_4k_read)

                # 校验4K随机写入速度
                if index == 5:
                    self.check_func(data_list, row, self.random_4k_write)
        self.re_write(data_list)

    def comp_512(self):
        data_list = []
        with open(self.report_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for index, row in enumerate(reader):
                # 取出需要校验的数据与标准值进行比对
                # 校验顺序读取速度
                if index == 0:
                    self.check_func(data_list, row, self.seq_read)
                # 校验顺序写入速度
                if index == 1:
                    self.check_func(data_list, row, self.seq_write)

                # 校验4K随机读取速度
                if index == 2:
                    self.check_func(data_list, row, self.random_4k_read)

                # 校验4K随机写入速度
                if index == 3:
                    self.check_func(data_list, row, self.random_4k_write)
        self.re_write(data_list)

    #校验函数
    def check_func(self, data_list, row, ty):
        if float(row['Speed']) < ty:
            print(row['Testing'] + row['Speed'] + 'MB/S' + '异常')
            list1 = [row['Testing'], row['Speed'], '异常']
            data_list.append(list1)
        else:
            print(row['Testing'] + row['Speed'] + 'MB/S' + '正常')
            list1 = [row['Testing'], row['Speed'], '正常']
            data_list.append(list1)

        #重写csv文件
    def re_write(self, list):
        with open(self.report_path, 'w+', encoding='utf-8', newline='') as f:
            headers = ['Testing', 'Speed(MB/S)', 'performance']
            writer = csv.writer(f)
            writer.writerow(headers)
            for li in list:
                rows = [li[0], li[1], li[2]]
                writer.writerow(rows)



