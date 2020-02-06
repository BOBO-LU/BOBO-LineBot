"""
代辦事項:
1. 對話模式切換，有點像是shell中開啟vim，進入該模式中直到離開前，會有另外一個filter來處理這些訊息。(可能要用到multi-thread)
2. 模式流程
訊息判斷(views) > 模式過濾(mode) > 文字過濾(text) 

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

from module import bullshit, stock

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)

def text_mode_filter(event):

    text = event.message.text.lower()
    userid = event.source.user_id
    #檢查資料庫是否有userid，沒有的話插入
    if not users.objects.filter(uid=userid).exists():
        unit = users.objects.create(uid=userid, mode="none")
        unit.save()

    temp = users.objects.filter(uid=userid)
    print('temp : ', temp)
    print('temp.value() : ', temp.values('chat_mode'))
    print('list(temp) : ', list(temp))
    for case in switch(temp):
        
        if case('stock'):
            stock_mode()
            break
        if case():
            normal_mode(event, text, userid)
            break

    
def stock_mode():
    print('in stock mode')

#針對不同文字處理不同訊息
def normal_mode(event, text, userid): 
    # try:
    #     if text[0] == ('s' or 'S'):
            
    #         
            
        
    # except Exception as _e:
    #     print(_e)

    try:
        for case in switch(text):
            if case('s' or 'S'):
                users.objects.filter(uid=userid).update(chat_mode="stock")
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text='進入stock模式'))
                break
            if case('b' or 'B'):
                content = str(bullshit.bullshit())
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=content))
                #push_text_message(userid,""+content)
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
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=event.message.text)) #回應同一個訊息
                #line_bot_api.push_message('U4f9b4c95fcee10fc8c72ad40cbef90ca', TextSendMessage(text=event.message.text+", send by "+event.source.user_id))
                #line_bot_api.reply_message(event.reply_token, TextSendMessage(text=event.message.text+'2'))
                break

    except Exception as e:
        print("exception")
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
