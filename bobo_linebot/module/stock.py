"""
代辦事項:
1. text_filter過濾出文字，stock.py滿足資料
"""
from application.tools import switch
from bs4 import BeautifulSoup
import requests

def stock_filter():

    """
    for case in switch(info):
        if case('last_close'):
            print(data_row[7].text)
            break
        if case('open_price'):
            print(data_row[8].text)
            break
        if case('high_price'):
            print(data_row[9].text)
            break
        if case('low_price'):
            print(data_row[10].text)
            break
        if case('close_price'):
            print(data_row[2].text)
            break
        """
    return ""

def yahoo_stock_crawler( stock_id = '2330'):
    url = 'https://tw.stock.yahoo.com/q/q?s='+stock_id
    doc = requests.get(url)
    html = BeautifulSoup(doc.text, 'html.parser')
    # 搜尋整個網頁裡，內容為 '個股資料' 的 html 標籤, 關聯到 table 最外層
    table = html.findAll(text='個股資料')[0].parent.parent.parent
    # 找尋 table 裡第二個 tr 標籤內所有的 td 標籤
    data_row = table.select('tr')[1].select('td')
    # 選取該 row 第八個 td 標籤，擷取標籤內文字

    for i in range(0,12):
        print(i,":",data_row[i].text)

    # last_close = data_row[7].text
    # print(f"台積電昨日收盤價：${last_close}")
    # return f"${stock_id}昨日收盤價：${last_close}"
    return {
        "open_price": data_row[8].text, #開盤
        "high_price": data_row[9].text, #最高
        "low_price": data_row[10].text, #最低
        "close_price": data_row[2].text, #成交
        "last_close": data_row[7].text #昨日收盤
    }