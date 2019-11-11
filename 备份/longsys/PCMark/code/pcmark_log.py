import os
from bs4 import BeautifulSoup
import lxml


class PcMarkLog(object):
    def __init__(self, log_path, rep_path, log_name):
        self.log_path = log_path
        self.log_name = log_name
        self.rep_path = rep_path

    def data_clean(self):
        print('提取日志文件关键字段...')
        path = self.log_path + self.log_name
        with open(path, 'r', encoding='utf-8') as f:
            r = f.read()
        b = BeautifulSoup(r, 'xml')

        # 将各项指标提取存进字典
        data_dict = {}
        data_dict['storage_score'] = b.find('storage_score').text
        data_dict['storage_bandwidth'] = b.find('storage_bandwidth').text
        data_dict['storage_world_of_warcraft'] = b.find('storage_world_of_warcraft_compound_s').text
        data_dict['storage_battlefield'] = b.find('storage_battlefield_3_compound_s').text
        data_dict['storage_adobe_photoshop_light'] = b.find('storage_adobe_photoshop_light_compound_s').text
        data_dict['storage_adobe_photoshop_heavy'] = b.find('storage_adobe_photoshop_heavy_compound_s').text
        data_dict['storage_adobe_indesign'] = b.find('storage_adobe_indesign_compound_s').text
        data_dict['storage_adobe_after_effects'] = b.find('storage_adobe_after_effects_compound_s').text
        data_dict['storage_adobe_illustrator'] = b.find('storage_adobe_illustrator_compound_s').text
        data_dict['storage_microsoft_word'] = b.find('storage_microsoft_word_compound_s').text
        data_dict['storage_microsoft_excel'] = b.find('storage_microsoft_excel_compound_s').text
        data_dict['storage_microsoft_powerpoint'] = b.find('storage_microsoft_powerpoint_compound_s').text

        # 将数据保存到txt文件
        self.write_data(data_dict)
        print('提取保存完毕...')

    def write_data(self, data_dict):
        rep_name = self.log_name.replace('xml','txt')
        rep_path = os.path.join(self.rep_path+rep_name)
        with open(rep_path, 'a+', encoding='utf-8') as f:
            for data in data_dict:
                if data == 'storage_score' or data == 'storage_bandwidth':
                    f.write(data+' : '+data_dict[data]+'\n')
                else:
                    f.write(data+' : '+data_dict[data]+' s '+'\n')
