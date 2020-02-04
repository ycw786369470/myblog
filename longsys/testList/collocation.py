import xlrd
from device_manage.models import Collocation
import os


def main():
    file_path = os.path.abspath('..') + '/static/media/excel_data/SN编码规则_1231.xlsx'
    print(file_path)
    data = xlrd.open_workbook(file_path)
    start_row = 1
    # 主控表
    sheet1 = data.sheets()[1]
    end_row1 = sheet1.nrows
    for i in range(start_row, end_row1):
        data = sheet1.row_values(i)
        collocate = Collocation()
        collocate.collocation = data[0]
        collocate.num = data[1]
        collocate.category = 0
        collocate.save()

    # flash表
    sheet2 = data.sheets()[2]
    end_row2 = sheet2.nrows
    for i in range(start_row, end_row2):
        data = sheet2.row_values(i)
        collocate = Collocation()
        collocate.collocation = data[1]
        collocate.abbreviation = data[2]
        collocate.num = data[3]
        collocate.category = 1
        collocate.save()

    # 容量表
    sheet3 = data.sheets()[3]
    end_row3 = sheet3.nrows
    for i in range(start_row, end_row3):
        data = sheet3.row_values(i)
        if len(data[0]) != 0:
            die = Collocation()
            die.collocation = data[0]
            die.num = data[1]
            die.category = 2
            die.save()
            cap = Collocation()
            cap.collocation = data[2]
            cap.num = data[3]
            cap.category = 4
            cap.save()
        else:
            cap = Collocation()
            cap.collocation = data[2]
            cap.num = data[3]
            cap.category = 4
            cap.save()
