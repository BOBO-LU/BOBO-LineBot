from django.conf import settings
from linebot import LineBotApi
from linebot.models import TextSendMessage, ImageSendMessage

import requests
import random
import re
from bs4 import BeautifulSoup
import xlwings as xw

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
PTT_url = "https://www.ptt.cc"


def get_webPage(url):
    res = requests.get(url,cookies = {'over18': '1'})
    return res.text

def get_articles(page):

    divs = page.select('.r-ent')
    hrefAll=[]
    for article in divs:
        if article.find('a'):
            href = article.find('a')['href']
            hrefAll.append(href)
                    
    nums=random.randint(1,19)
    return hrefAll[nums]

def get_image(artic):
        
    res = requests.get(f'https://www.pttweb.cc{artic}')
    html=BeautifulSoup(res.text,"html.parser")
    imgLinks = html.findAll('a',{'class':'externalHref'})
    img=imgLinks[0].text
    return img

def sendImage(event):

    wb = xw.Book("pttBeauty.xlsx")
    sheet = wb.sheets["beauty1"]


    final = sheet.range("B2").value


    try:
        message = ImageSendMessage(
            original_content_url= final,
            preview_image_url=final
        )
        line_bot_api.reply_message(event.reply_token,message)
        print(final)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='運氣真差 再抽一次'))

   
    while 1:
        num=random.randint(1000,3026)
        #print(num)
        content=get_webPage(f'{PTT_url}/bbs/Beauty/index{num}.html')
        html=BeautifulSoup(content,"html.parser")
        girl=get_articles(html)
        sheet.range("B2").value = get_image(girl)

        txt = sheet.range("B2").value
        x = txt.find("https://i.imgur.com")
        if x != -1:
            break