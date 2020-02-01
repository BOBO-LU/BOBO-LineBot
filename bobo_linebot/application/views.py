from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage, TextMessage, ImageSendMessage

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)

@csrf_exempt
def callback(request):

    if ( request.method == 'POST' ):
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')

        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
        
        for event in events:
            if isinstance(event, MessageEvent):
                if isinstance(event.message, TextMessage):
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=event.message.text)) #回應同一個訊息
                    userid = event.source.user_id
                    line_bot_api.push_message('U4f9b4c95fcee10fc8c72ad40cbef90ca', TextSendMessage(text=event.message.text+", send by "+event.source.user_id))
                    line_bot_api.push_message(userid, TextSendMessage(text=event.message.text+", send by "+event.source.user_id))
        return HttpResponse()
    else:
        return HttpResponseBadRequest() 


# def push_message(request):
#     try:
#         line_bot_api.push_message('<to>', TextSendMessage(text=event.message.text))
#     except LineBotApiError as e:
#         print(e)

