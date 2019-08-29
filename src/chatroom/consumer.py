from django.contrib.auth import get_user_model
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from .models import Message

User = get_user_model()

class ChatConsumer(WebsocketConsumer):

    def fetch_msgs(self,data):
        msgs = Message.last_10_msgs()
        content = {
            'messages': self.msgs_to_json(msgs)
        }
        self.send_message(content)

    def new_msgs(self,data):
        author = data['from']
        author_user = User.objects.filter(username=author)[0]
        message = Message.objects.create(
            author= author_user,
            content= data['message'])
        message.save()
        content = {
            'message': self.msg_to_json(message)
        }
        return self.send_chat_messages(content)

    def msgs_to_json(self,msgs):
        result = []
        for msg in msgs:
            result.append(self.msg_to_json(msg))
        print(result)
        return result
    
    def msg_to_json(self,msg):
        return {
            'author': msg.author.username,
            'content': msg.content,
            'timestamp': str(msg.timestamp)
        }

    commands = {
        'fetch_msgs': fetch_msgs,
        'new_msgs': new_msgs
    }

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self,data)

    def send_chat_messages(self,message):
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def send_messages(self,msgs):
        self.send(text_data=json.dumps(msgs))

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        print(message)
        # Send message to WebSocket
        self.send(text_data=json.dumps(message))