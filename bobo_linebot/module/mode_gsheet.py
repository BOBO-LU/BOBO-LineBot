import pygsheets
from pyquery import PyQuery as pq
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36'}

def get_web_title(url):
    """取得網頁Title"""
    try:
        doc = pq(url=url, encoding='utf-8', headers=HEADERS)
        print("type:",type(doc))
        print(doc)
        print(doc('title').text())
        return doc('title').text()
    except Exception as e2:
        print("$$$ Pyquery Exception $$$")
        doc = get_web_title_selenium(url)
        return doc
    
def get_web_title_selenium(url):
    webdriver_path = "C:\\Users\\呂文楷\\Desktop\\BOBO LineBot\\bobo_linebot\\bobo_linebot\\chromedriver.exe"
    options = Options()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--test-type')
    #options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(executable_path=webdriver_path, options=options)

    try:
        driver.get(url)
        print("## set URL ")
        title = driver.find_element_by_tag_name('title').text
        print(title)
        driver.close()
    except Exception as e:
        return "error"
    
    
def update_googlesheet(url='none'):
    """上傳字串至google sheet"""

    #取得網頁標題
    title = get_web_title(url)

    # 驗證
    gc = pygsheets.authorize(service_file=r"C:\\Users\\呂文楷\\Desktop\\BOBO LineBot\\bobo_linebot\\bobo_linebot\\learned-ocean-268201-24e7267e7e4a.json")
    print("gc:", gc)

    #選擇gsheet
    workbook = gc.open_by_url("https://docs.google.com/spreadsheets/d/1Puwzr2Ov5qf0sIQ2nchgFwAVwSASASzNp0wQrzJgcq0/edit#gid=0")
    print("workbook:", workbook)
    print("workbook.url:", workbook.url)

    # 選擇追蹤清單
    work_sheet = workbook.worksheet_by_title("autorun test")
    print("work_sheet:", work_sheet)

    # 偵測該工作表最後一個 row
    col_a_data = work_sheet.get_col(3, include_tailing_empty=False)
    last_row = str(len(col_a_data)+1)
    print(last_row)

    # wks.insert_rows(row=last_row, values=['https'])
    location_title = 'B'+last_row
    location_url = 'C'+last_row
    work_sheet.update_value(location_title, title)
    work_sheet.update_value(location_url, url)

# update_googlesheet('test')
# get_web_title('https://www.edntaiwan.com/news/article/20170918nt02-counterfeit-ai-deep-learning')
# get_web_title_selenium('https://www.edntaiwan.com/news/article/20170918NT02-counterfeit-AI-deep-learning')