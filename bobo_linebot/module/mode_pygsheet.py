
import pygsheets
# 驗證
gc = pygsheets.authorize(service_file=r"C:\\Users\\USER\\Desktop\\a資料\\python\\練習\\BOBO-LineBot\\bobo_linebot\\bobo_linebot\\learned-ocean-268201-24e7267e7e4a.json")
print("gc:",gc)

#選擇gsheet
wb = gc.open_by_url("https://docs.google.com/spreadsheets/d/1Puwzr2Ov5qf0sIQ2nchgFwAVwSASASzNp0wQrzJgcq0/edit#gid=0")
print("wb:",wb)
print("wb.url:",wb.url)

# 選擇追蹤清單
wks = wb.worksheet_by_title("autorun test")
print("wks:",wks)

# 偵測該工作表最後一個 row
col_a_data = wks.get_col(1, include_tailing_empty=False)
last_row = len(col_a_data)+1
print(last_row)

# wks.insert_rows(row=last_row, values=['https'])
location = 'D'+str(last_row)
wks.update_value(location,'bobo')