"""
代辦事項:
1. 對話模式切換，有點像是shell中開啟vim，進入該模式中直到離開前，會有另外一個filter來處理這些訊息。(可能要用到multi-thread)
2. 模式流程

訊息判斷(views) > 模式過濾(text_mode_filter) > 文字過濾(text) > 對應功能 

需求:
1. 輸入指令，進入特殊模式，產生新的對應指令
2. 可以離開模式
3. 輸入h可以顯示幫助內容
4. 快速切換模式

"""
from time import sleep
from django.conf import settings
from linebot import LineBotApi
from linebot.models import (
    TextSendMessage, ImageSendMessage, LocationSendMessage,
    QuickReply, QuickReplyButton, MessageAction,
    CameraAction, DatetimePickerAction
)

from application.tools import switch, getException
from application.models import users

from module import mode_bullshit, mode_stock

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)

def text_mode_filter(event):

    text = event.message.text.lower()
    userid = event.source.user_id

    #檢查資料庫是否有userid，沒有的話插入
    if not users.objects.filter(uid=userid).exists():
        unit = users.objects.create(uid=userid, chat_mode="none")
        unit.save()

    #取得userid在資料庫中chat_mode的欄位
    mode = users.objects.filter(uid=userid).values('chat_mode')[0]['chat_mode']

    for case in switch(mode):
        if case('stock'):
            stock_mode(event, text, userid, mode)
            break
        if case('bullshit'):
            bullshit_mode(event, text, userid, mode)
            break
        if case():
            normal_mode(event, text, userid)
            break

def bullshit_mode(event, text, userid, mode):
    print('in bullshit mode, text = ',text)
    for case in switch(text):
        if case('l'):
            leave_mode(event, text, userid, mode)
            break
        if case('h'):
            help_content = "離開模式: L或l\n查看模式: M或m\n----\n產生幹話: {主題}\n指定長度: {主題},{長度}\n像是: 機器人,100"
            reply_text(event, help_content)
            break
        if case('m'):
            reply_text(event, mode+' mode')
            break
        if case():
            content = str(mode_bullshit.bullshit(text))
            reply_text(event, content)
            break
        

def stock_mode(event, text, userid, mode):
    print('in stock mode, text = ',text)
    for case in switch(text):
        if case('l'):
            print('L in stock mode')
            leave_mode(event, text, userid, mode)
            break
        if case('h'):
            help_content = "離開模式: L或l\n查看模式: M或m\n----"
            reply_text(event, help_content)
            break
        if case('m'):
            reply_text(event, mode+' mode')
            break
        if case():
            break

#針對不同文字處理不同訊息
def normal_mode(event, text, userid): 
    try:
        for case in switch(text):
            if case('s'): #進入stock模式
                users.objects.filter(uid=userid).update(chat_mode="stock")
                content = '進入股票模式'
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=content))
                break
            if case('b'):#進入bullshit模式
                #content = str(bullshit.bullshit())
                users.objects.filter(uid=userid).update(chat_mode="bullshit")
                content = "進入唬爛模式\n請輸入主題名稱:(離開模式輸入L或l)"
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=content))
                break
            
            if case('userid'):
                push_text(userid, "userid : "+event.source.user_id)
                push_text('U4f9b4c95fcee10fc8c72ad40cbef90ca',event.message.text+", send by "+event.source.user_id)
                break
            if case('test'):
                push_text(userid, 'test')
                break
            if case('肚子餓') and userid != 'U715b0aba205ddf78123b47ffb8f28f52': #如果是妹妹，就不能說不好的話
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text='乾我什麼事'))
                break
            if case('變身'):
                push_image(userid, 'https://i.imgur.com/zTbh6K1.jpg', 'https://i.imgur.com/CNhnRs2.jpg')
                break
            if case('小火龍'):
                push_image(userid, 'https://i.imgur.com/zTbh6K1.jpg', 'https://i.imgur.com/zTbh6K1.jpg')
                break
            if case('等'):
                sleep(20)
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text='乾我什麼事'))
                break
            if case('q'):
                message = TextSendMessage(
                    text=" i am bobo",
                    quick_reply=QuickReply(
                        items=[
                            QuickReplyButton(
                                action=MessageAction(label='LOVE', text='LOVE')
                            ),
                            QuickReplyButton(
                                image_url="https://i.ibb.co/dJPnTr9/pika-icon.png",
                                action={
                                "type": "message",
                                "label": "Tempura",
                                "text": "PIKACHU"
                                }
                            ),
                            QuickReplyButton(
                                image_url="https://i.ibb.co/dJPnTr9/pika-icon.png",
                                action={
                                "type": "message",
                                "label": "Tempura",
                                "text": "PIKACHU"
                                }
                            ),
                            QuickReplyButton(action=
                                {
                                "type":"camera",
                                "label":"Camera"
                                }
                            ),
                            QuickReplyButton(
                                action=DatetimePickerAction(label="depart date", data="data3", mode="date")
                            ),
                            QuickReplyButton(
                                action=DatetimePickerAction(label="depart time", data="data3", mode="time")
                            )
                        ]
                    )
                )
                
                line_bot_api.reply_message(event.reply_token, message)
                break
            if case('push'):
                push_text('Udd66eba9352626779fee2fff43c79f82', 'i am bobo') #蕭瑞昕的ID
                break
            if case():
                print(event.reply_token)
                reply_text(event, event.message.text) #回應同一個訊息
                #line_bot_api.push_message('U4f9b4c95fcee10fc8c72ad40cbef90ca', TextSendMessage(text=event.message.text+", send by "+event.source.user_id))
                #line_bot_api.reply_message(event.reply_token, TextSendMessage(text=event.message.text+'2'))
                break

    except Exception as e:
        print("exception")
        getException(e)

def leave_mode(event, text, userid, mode):
    users.objects.filter(uid=userid).update(chat_mode="none")
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text='離開'+mode+'模式'))

def reply_text(event, text):
    try:
        message = TextSendMessage(text=text)
        token = event.reply_token
        line_bot_api.reply_message(token, message)
    except Exception as e:
        getException(e)

def reply_image(event, original, preview):
    try:
        message = ImageSendMessage(
            original_content_url = original,
            preview_image_url = preview
        )
        token = event.reply_token
        line_bot_api.reply_message(token, message)
    except Exception as e:
        getException(e)

def reply_sticker(event, package = 1, sticker = 1):
    try:
        message = ImageSendMessage(
            package_id = package,
            sticker_id = sticker
        )
        token = event.reply_token
        line_bot_api.reply_message(token, message)
    except Exception as e:
        getException(e)

def reply_location(event, title="", address="", latitude=0.0, longtitude=0.0):
    try:
        message = LocationSendMessage(
            title=title,
            address=address,
            latitude=latitude,
            longtitude=longtitude
        )
        token = event.reply_token
        line_bot_api.push_message(token, message)
    except Exception as e:
        getException(e)

def push_text(userid, text):
    try:
        message = TextSendMessage(text=text)
        line_bot_api.push_message(userid, message)
    except Exception as e:
        getException(e)

def push_image(userid, original, preview):
    try:
        message = ImageSendMessage(
            original_content_url = original,
            preview_image_url = preview
        )
        line_bot_api.push_message(userid, message)
    except Exception as e:
        getException(e)

def push_sticker(userid, package = 1, sticker = 1):
    try:
        message = ImageSendMessage(
            package_id = package,
            sticker_id = sticker
        )
        line_bot_api.push_message(userid, message)
    except Exception as e:
        getException(e)

def push_location(userid, title="", address="", latitude=0.0, longtitude=0.0):
    try:
        message = LocationSendMessage(
            title=title,
            address=address,
            latitude=latitude,
            longtitude=longtitude
        )
        line_bot_api.push_message(userid, message)
    except Exception as e:
        getException(e)

def push_quickreply(userid, buttons):
    try:
        for i in buttons:
            print(i)
        message = TextSendMessage(
            text = "i am bobo",
            quick_reply = QuickReply(
                items = [
                    QuickReplyButton(
                        action = MessageAction(label = 'but1', text = 'text1')
                    ),
                    QuickReplyButton(
                        action = MessageAction(label = 'but2', text = 'text2')
                    ),
                    QuickReplyButton(
                        action = CameraAction('camera')
                    )
                ]
            )
        )
        line_bot_api.push_message(userid, message)
    except Exception as e:
        getException(e)

