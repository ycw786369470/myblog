from selenium import webdriver
import time
import pymysql


class GanJi(object):
    def __init__(self):
        self.url = 'http://cs.ganji.com/zufang/b3/'
        self.driver = webdriver.Chrome()

    # 进入12306
    def goto_web(self):
        self.driver.get(self.url)
        self.driver.maximize_window()
        self.driver.maximize_window()

    def get_data(self):
        name_ls = self.driver.find_elements_by_xpath('//dl[@class="f-list-item-wrap min-line-height f-clear"]/dd/a')
        names = [i.text for i in name_ls]

        inform_ls = self.driver.find_elements_by_xpath('//dl[@class="f-list-item-wrap min-line-height f-clear"]/dd[@class="dd-item size"]')
        types = []
        sizes = []
        for i in inform_ls:
            types.append(i.find_element_by_xpath('.//span[1]').text)
            sizes.append(i.find_element_by_xpath('.//span[3]').text)

        area_ls = self.driver.find_elements_by_xpath('//dl[@class="f-list-item-wrap min-line-height f-clear"]/dd/span[@class="area"][1]')
        areas = [j.text for j in area_ls]

        price_ls = self.driver.find_elements_by_class_name('price')
        prices = [m.text for m in price_ls]

        data_dict = {
            'name': names,
            'inform': types,
            'size': sizes,
            'area': areas,
            'price': prices
        }

        return data_dict


class PyMySQL(object):
    def __init__(self):
        self.root = 'root'
        self.pswd = '123'
        self.name = 'ganji'

    def link_database(self):
        self.db = pymysql.connect('localhost', self.root, self.pswd, self.name)
        print('连接数据库成功')
        self.cursor = self.db.cursor()

    def save_to_sql(self, data):
        names = data.get('name')
        informs = data.get('inform')
        sizes = data.get('size')
        areas = data.get('area')
        prices = data.get('price')
        for i in range(len(names)):
            name = names[i]
            inform = informs[i]
            size = sizes[i]
            area = areas[i]
            price = prices[i]
            sql = f'insert into data(name, inform, size, area, price) values("{name}", "{inform}", "{size}", "{area}", "{price}");'
            self.cursor.execute(sql)
            print(f'第{i}条数据保存完毕')
        print('保存完毕！')


if __name__ == '__main__':
    # 初始化爬虫程序
    ganji = GanJi()
    # 初始化数据库
    sql = PyMySQL()
    # 连接数据库
    sql.link_database()
    # 前往爬取的网页
    ganji.goto_web()
    # 提取数据
    data = ganji.get_data()
    # 保存数据
    sql.save_to_sql(data)