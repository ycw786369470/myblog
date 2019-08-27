from selenium import webdriver
from bs4 import BeautifulSoup
import urllib.request

class GetPicture(object):
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.url = 'https://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&word=%E5%AD%99%E7%AC%91%E5%B7%9D'
        self.path = '../imgs/'

    def go_to_page(self):
        self.driver.get(self.url)
        html = self.driver.page_source
        self.driver.close()
        self.driver.quit()
        # self.save_data(html)
        return html

    def get_pic_src(self, html):
        num = 1
        soup = BeautifulSoup(html, 'lxml')
        img_ls = soup.find_all('img', class_='main_img img-hover')
        for img in img_ls:
            img_src = img['src']
            self.down_load_img(img_src, num)
            num += 1

    def save_data(self, data):
        with open('../htmls/sxcimg.html', 'a', encoding='utf-8') as f:
            f.write(data)
            f.write('\n')

    def down_load_img(self, img_src, name):
        urllib.request.urlretrieve(img_src, filename='{}{}.jpg'.format(self.path, str(name)))




if __name__ == '__main__':
    pict = GetPicture()
    # 使用selenim取得html并分析.
    html = pict.go_to_page()
    pict.get_pic_src(html)