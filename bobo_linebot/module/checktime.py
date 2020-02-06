import time
import datetime as dt

#執行checktime會直接進入迴圈，如果電腦時間和需求時間一樣，會跳出來
"""
代辦事項:
1.multi-thread 讓迴圈去其他thread等待
2.可以在資料庫中客制化設定hour 和 minute
"""

class checktime():
    def __init__ (self, hour=21, minute=2):
        #設定常數時間
        self.hour = hour #24小時制
        self.minute = minute

    def checktime(self):
        while True:
            if ( dt.datetime.now().hour == self.hour and dt.datetime.now().minute == self.minute):

                #do something
                print("bobo",dt.datetime.now())
                #finish do something

                break
            else:
                print( dt.datetime.now().hour, dt.datetime.now().minute, dt.datetime.now().second)
                time.sleep(30)



"""
import time

time.strftime("%Y/%m/%d")
""" 