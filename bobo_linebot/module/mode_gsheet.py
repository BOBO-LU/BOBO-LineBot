import pygsheets


def update_googlesheet(url='none'):
    # 驗證
    gc = pygsheets.authorize(service_file=r"C:\\Users\\呂文楷\\Desktop\\BOBO LineBot\\bobo_linebot\\bobo_linebot\\learned-ocean-268201-24e7267e7e4a.json")
    print("gc:", gc)

    #選擇gsheet
    workbook = gc.open_by_url("https://docs.google.com/spreadsheets/d/1Puwzr2Ov5qf0sIQ2nchgFwAVwSASASzNp0wQrzJgcq0/edit#gid=0")
    print("workbook:", workbook)
    print("workbook.url:", workbook.url)

    # 選擇追蹤清單
    work_sheet = workbook.worksheet_by_title("科技新聞")
    print("work_sheet:", work_sheet)

    # 偵測該工作表最後一個 row
    col_a_data = work_sheet.get_col(3, include_tailing_empty=False)
    last_row = len(col_a_data)+1
    print(last_row)

    # wks.insert_rows(row=last_row, values=['https'])
    location = 'C'+str(last_row)
    work_sheet.update_value(location, url)

# update_googlesheet('test')