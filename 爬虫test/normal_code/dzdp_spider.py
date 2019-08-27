import requests
from bs4 import BeautifulSoup
import json

class Dazhong(object):
    def __init__(self):
        # self.city_name = city_name
        # 存放所有url
        self.ls_urls = []
        self.url = 'http://www.dianping.com/mylist/ajax/shoprank?rankId=c950bc35ad04316c76e89bf2dc86bfe064d8acadd74fe416da09a4c05d7f8e51'

        self.header = {'User-Agent': '"Mozilla/5.0', 'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'Connection': 'keep-alive',
                  'Cookie': '_lxsdk_cuid=16b830dca85c8-01ce44d725c41c-6353160-144000-16b830dca85c8; _lxsdk=16b830dca85c8-01ce44d725c41c-6353160-144000-16b830dca85c8; _hc.v=fb97e8e4-c958-a62a-7da7-11c901ea66f3.1561271848; s_ViewType=10; aburl=1; _dp.ac.v=e8398446-6e67-4a82-9eca-051e5684efa6; dper=eb3847c7c5d0776092dfdd7a16ef493cbee24ff62a365baa194fe70899ab6941245b72d77289362a60ae02bef1a075e8bf3d3da3dd1d50f65c3dab95fd808af048e9ea538ed61e3408c9c606d1c92f5eab68055ee31c5205b48f477851e81f5c; ua=dpuser_3799590584; ctu=8c8354b200c404d916102afcf7aac6a56282e37bacc612acab492410b3335ebd; ll=7fd06e815b796be3df069dec7836c3df; cy=8; cye=chengdu; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; _lxsdk_s=16c4bfb5ebc-f30-29c-5f9%7C%7C66',
        }
        self.data = {'rankId': 'c950bc35ad04316c76e89bf2dc86bfe064d8acadd74fe416da09a4c05d7f8e51'}

    def run(self):
        res = requests.post(self.url, headers=self.header, data=self.data).content
        print(res)
        # with open('../htmls/{}food.html'.format(self.city_name), 'w+', encoding='utf-8') as f:
        #     f.write(res)

if __name__ == '__main__':
    # name = input('输入城市名字>>>')
    dazhong = Dazhong()
    dazhong.run()
