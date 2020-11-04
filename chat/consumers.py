
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
from asgiref.sync import async_to_sync
import json

class ChatRoomConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope['user']
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()
        print(self.channel_name+"Connect")
  
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
        print(self.channel_name+"DisConnect")
    def receive(self, text_data=None, bytes_data=None):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type':'sendTo_group',
                'msg':text_data

            }
        )

    def sendTo_group(self,event):
        sendbackmsg = event['msg']
        self.send(json.dumps({'serverMsg':sendbackmsg,'username':self.user.username}))