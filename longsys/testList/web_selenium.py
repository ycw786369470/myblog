from selenium import webdriver
import time as t


class Chrome(object):
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.url = 'http://web.airdisk.cc/'
        self.driver.implicitly_wait(30)         # 隐性等待，最长等30秒

    def go_web(self):
        self.driver.get(self.url)
        self.driver.maximize_window()

    def login(self):
        username = self.driver.find_element_by_name('PhoneNo')
        password = self.driver.find_element_by_name('Pwd')
        username.click()
        username.send_keys('15692081987')
        t.sleep(1)
        password.click()
        password.send_keys('damai888')
        t.sleep(1)
        login_btn = self.driver.find_element_by_class_name('login_btn')
        login_btn.click()

    def choose_device(self):
        device_li = self.driver.find_element_by_xpath('//*[@id="app"]/div[1]/div[2]/div[2]/div[2]/div[2]/ul/li[28]')
        device_li.click()


def main():
    web = Chrome()
    web.go_web()
    web.login()
    web.choose_device()
    t.sleep(5)


if __name__ == '__main__':
    main()