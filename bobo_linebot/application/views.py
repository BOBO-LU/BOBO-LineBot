from application.tools import switch

from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookParser, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageAction,
    ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn, URIAction,
    PostbackAction, DatetimePickerAction,
    CameraAction, CameraRollAction, LocationAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, VideoMessage, AudioMessage, FileMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent,
    #MemberJoinedEvent, MemberLeftEvent,
    FlexSendMessage, BubbleContainer, ImageComponent, BoxComponent,
    TextComponent, SpacerComponent, IconComponent, ButtonComponent,
    SeparatorComponent, QuickReply, QuickReplyButton,
    ImageSendMessage)

from module import func
import logging

logger = logging.getLogger(__name__)
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(settings.LINE_CHANNEL_SECRET)

@csrf_exempt
def callback(request):
    if ( request.method == 'POST' ):
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError as e:
            print("Got exception from LINE Messaging API: %s\n" % e.message)
            for m in e.error.details:
                print("  %s: %s\n" % (m.property, m.message))
            print("\n")
            return HttpResponseBadRequest()

        return HttpResponse()
    else:
        return HttpResponseBadRequest() 

@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    func.text_mode_filter(event)

@handler.add(MessageEvent, message=LocationMessage)
def handle_location_message(event):
    print('receive location message')

@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        StickerSendMessage(
            package_id=event.message.package_id,
            sticker_id=event.message.sticker_id)
    )

# @handler.add(MessageEvent, message=(ImageMessage, VideoMessage, AudioMessage))
# def handle_content_message(event):
#     if isinstance(event.message, ImageMessage):
#         ext = 'jpg'
#     elif isinstance(event.message, VideoMessage):
#         ext = 'mp4'
#     elif isinstance(event.message, AudioMessage):
#         ext = 'm4a'
#     else:
#         return

#     message_content = line_bot_api.get_message_content(event.message.id)
#     with tempfile.NamedTemporaryFile(dir=static_tmp_path, prefix=ext + '-', delete=False) as tf:
#         for chunk in message_content.iter_content():
#             tf.write(chunk)
#         tempfile_path = tf.name

#     dist_path = tempfile_path + '.' + ext
#     dist_name = os.path.basename(dist_path)
#     os.rename(tempfile_path, dist_path)

#     line_bot_api.reply_message(
#         event.reply_token, [
#             TextSendMessage(text='Save content.'),
#             TextSendMessage(text=request.host_url + os.path.join('static', 'tmp', dist_name))
#         ])


# @handler.add(MessageEvent, message=FileMessage)
# def handle_file_message(event):
#     message_content = line_bot_api.get_message_content(event.message.id)
#     with tempfile.NamedTemporaryFile(dir=static_tmp_path, prefix='file-', delete=False) as tf:
#         for chunk in message_content.iter_content():
#             tf.write(chunk)
#         tempfile_path = tf.name

#     dist_path = tempfile_path + '-' + event.message.file_name
#     dist_name = os.path.basename(dist_path)
#     os.rename(tempfile_path, dist_path)

#     line_bot_api.reply_message(
#         event.reply_token, [
#             TextSendMessage(text='Save file.'),
#             TextSendMessage(text=request.host_url + os.path.join('static', 'tmp', dist_name))
#         ])


@handler.add(FollowEvent)
def handle_follow(event):
    logger.info("Got Follow event:" + event.source.user_id)
    line_bot_api.reply_message(
        event.reply_token, TextSendMessage(text='Got follow event'))


@handler.add(UnfollowEvent)
def handle_unfollow(event):
    logger.info("Got Unfollow event:" + event.source.user_id)


@handler.add(JoinEvent) 
def handle_join(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='Joined this ' + event.source.type))


@handler.add(LeaveEvent)
def handle_leave():
    logger.info("Got leave event")


@handler.add(PostbackEvent)
def handle_postback(event):
    if event.postback.data == 'ping':
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='pong'))
    elif event.postback.data == 'datetime_postback':
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.postback.params['datetime']))
    elif event.postback.data == 'date_postback':
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.postback.params['date']))


@handler.add(BeaconEvent)
def handle_beacon(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(
            text='Got beacon event. hwid={}, device_message(hex string)={}'.format(
                event.beacon.hwid, event.beacon.dm)))


# @handler.add(MemberJoinedEvent)
# def handle_member_joined(event):
#     line_bot_api.reply_message(
#         event.reply_token,
#         TextSendMessage(
#             text='Got memberJoined event. event={}'.format(
#                 event)))


# @handler.add(MemberLeftEvent)
# def handle_member_left(event):
#     logger.info("Got memberLeft event")