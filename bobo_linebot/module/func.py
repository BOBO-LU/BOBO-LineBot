"""
代辦事項:
1. 對話模式切換，有點像是shell中開啟vim，進入該模式中直到離開前，會有另外一個filter來處理這些訊息。(可能要用到multi-thread)
"""
from application.tools import switch, getException
from django.conf import settings
from linebot import LineBotApi
from linebot.models import TextSendMessage, ImageSendMessage, LocationSendMessage, QuickReply, QuickReplyButton, MessageAction, CameraAction
from time import sleep
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)

#針對不同文字處理不同訊息
def text_filter(event): 
    text = event.message.text.lower()
    userid = event.source.user_id
    try:
        
        for case in switch(text):
            if case('userid'):
                push_text_message(userid,"userid : "+event.source.user_id)
                line_bot_api.push_message('U4f9b4c95fcee10fc8c72ad40cbef90ca', TextSendMessage(text=event.message.text+", send by "+event.source.user_id))
                break
            if case('test'):
                line_bot_api.push_message(userid, TextSendMessage(text='test'))
                break
            if case('肚子餓') and userid != 'U715b0aba205ddf78123b47ffb8f28f52': #如果是妹妹，就不能說不好的話
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text='乾我什麼事'))
                break
            if case('變身'):
                push_image_message(userid, 'https://i.imgur.com/zTbh6K1.jpg', 'https://i.imgur.com/CNhnRs2.jpg')
                break
            if case('小火龍'):
                push_image_message(userid, 'https://i.imgur.com/zTbh6K1.jpg', 'https://i.imgur.com/zTbh6K1.jpg')
                break
            if case('等'):
                sleep(20)
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text='乾我什麼事'))
                break
            if case('q'):
                message = TextSendMessage(
                    text = " i am bobo",
                    quick_reply = QuickReply(
                        items = [
                            QuickReplyButton(
                                action = MessageAction(label = 'LOVE', text = 'LOVE')
                            ),
                            QuickReplyButton(
                                image_url = "https://i.ibb.co/dJPnTr9/pika-icon.png",
                                action = {
                                "type": "message",
                                "label": "Tempura",
                                "text": "PIKACHU"
                                }
                            ),
                            QuickReplyButton(
                                image_url = "https://i.ibb.co/dJPnTr9/pika-icon.png",
                                action = {
                                "type": "message",
                                "label": "Tempura",
                                "text": "PIKACHU"
                                }
                            ),
                            QuickReplyButton(action = 
                                {
                                "type":"camera",
                                "label":"Camera"
                                }
                            )
                        ]
                    )
                )
                
                line_bot_api.reply_message(event.reply_token, message)
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


def push_text_message(userid, text):
    try:
        message = TextSendMessage(text=text)
        line_bot_api.push_message(userid, message)
    except Exception as e:
        getException(e)

def push_image_message(userid, original, preview):
    try:
        message = ImageSendMessage(
            original_content_url = original,
            preview_image_url = preview
        )
        line_bot_api.push_message(userid, message)
    except Exception as e:
        getException(e)

def push_sticker_message(userid, package = 1, sticker = 1):
    try:
        message = ImageSendMessage(
            package_id = package,
            sticker_id = sticker
        )
        line_bot_api.push_message(userid, message)
    except Exception as e:
        getException(e)

def push_location_message(userid, title = "", address = "", latitude = 0.0, longtitude = 0.0):
    try:
        message = LocationSendMessage(
            title = title,
            address = address,
            latitude = latitude,
            longtitude = longtitude
        )
        line_bot_api.push_message(userid, message)
    except Exception as e:
        getException(e)

def push_quickreply_message(userid, buttons):
    try:
        for i in buttons:
            print()
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

