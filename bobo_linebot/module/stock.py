from bs4 import BeautifulSoup
import requests

def find_stock_price( stock_id = '2330' ):
    url = 'https://tw.stock.yahoo.com/q/q?s='+stock_id
    doc = requests.get(url)
    html = BeautifulSoup(doc.text, 'html.parser')
    # 搜尋整個網頁裡，內容為 '個股資料' 的 html 標籤, 關聯到 table 最外層
    table = html.findAll(text='個股資料')[0].parent.parent.parent
    # 找尋 table 裡第二個 tr 標籤內所有的 td 標籤
    data_row = table.select('tr')[1].select('td')
    # 選取該 row 第八個 td 標籤，擷取標籤內文字
    last_close = data_row[7].text
    print(f"台積電昨日收盤價：${last_close}")
    return f"${stock_id}昨日收盤價：${last_close}"

text = '0123456789'
print(text[0:2])