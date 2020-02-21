"""
代辦事項:
1. webdriver_path 使用setting 裡面的base_dir代替
2. /help 內容(指令教學)
"""
from application.tools import switch, getException
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep



class bullshit():
    def __init__(self, topic = '機器人', length = 100):
        webdriver_path = "C:\\Users\\呂文楷\\Desktop\\BOBO-LineBot\\bobo-linebot\\bobo-linebot\\chromedriver.exe"
        weburl = "https://howtobullshit.me/" #前往這個網址

        options = Options()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--test-type')
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(executable_path=webdriver_path, options=options)

        self.content = ""
        if topic.find(',') != -1 :
            sp = topic.split(",")
            topic = sp[0]
            length = int(sp[1])

        elif topic.find('，') != -1:
            sp = topic.split("，")
            topic = sp[0]
            length = int(sp[1])

        try:
            driver.get(weburl) 
            print("## set URL ")
        except Exception as e:
            getException(e)

        try:
            driver.find_element_by_id('topic').send_keys(topic)
            # sleep(.5)
            driver.find_element_by_id('minlen').send_keys(length)
            # sleep(.5)
            driver.find_element_by_id('btn-get-bullshit').click()
            sleep(3)
            self.content = driver.find_element_by_id('content').text
            print(self.content)
        except Exception as e:
            getException(e)

        driver.close()
    # def generate(self):
        
    def __str__(self):
        return self.content
