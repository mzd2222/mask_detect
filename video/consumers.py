# video/consumers.py
import cv2
import numpy as np
import base64
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from yolov5 import mask_detect_img

encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 95]

class VideoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # channel_type = self.scope['url_route']['kwargs']['channel_name']
        self.room_name, channel_type = self.scope['url_route']['kwargs']['v_name'].split('_')
        self.room_group_name = 'video_%s_%s' % (self.room_name, channel_type)

        print("channel_name: " + self.channel_name)          # 自动生成
        print("room_name: " + self.room_name)                # 指定
        print("room_group_name: " + self.room_group_name)    # 指定
        # Join room group
        # print(self.channel_layer)
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):

        code, base64_data = text_data.split(',')
        # print(code)
        # print(img_msg)
        imgData = base64.b64decode(base64_data)
        nparr = np.fromstring(imgData, np.uint8)
        img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        frame, text = mask_detect_img.main_img(img_np)
        cv2.imshow('a', frame)
        cv2.waitKey(1)
        # result, imgencode = cv2.imencode('.jpg', frame, encode_param)
        # data = np.array(imgencode)
        # img = data.tobytes()
        # base64_data_after = base64.b64encode(img).decode()
        # text_data = "data:image/jpg;base64," + base64_data_after

        _, room_name, channel_type = self.room_group_name.split('_')
        room_group_name = 'video_%s_%s' % (self.room_name, 'output')

        await self.channel_layer.group_send(
            # 'video_output_channel',
            room_group_name,
            {
                'type': 'video_message',
                'message': text_data,
            }
        )

    # Receive message from room group
    async def video_message(self, event):
        # print(2)
        # print(event['type'])
        message = event['message']

        try:
            await self.send(text_data=json.dumps({
                'message': message}))
        except:
            pass
