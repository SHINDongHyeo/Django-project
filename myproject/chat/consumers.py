import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):

        # 채팅방(Room) 이름을 URL 매개변수에서 가져와서 사용
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_id = f"chat_{self.room_id}"
        
        # 채팅방 그룹에 참여
        await self.channel_layer.group_add(
            self.room_group_id,
            self.channel_name
        )
    
        await self.accept()

    async def disconnect(self, close_code):
        # 채팅방 그룹에서 나가기
        await self.channel_layer.group_discard(
            self.room_group_id,
            self.channel_name
        )
        

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        type = text_data_json['type']
        print(message, type)

        # 채팅방 그룹에 메시지 브로드캐스트
        await self.channel_layer.group_send(
            self.room_group_id,
            {
                'type': 'chat.message',
                'message': message,
                'mytype': type
            }
        )

  # 채팅방 그룹으로부터 메시지 수신
    async def chat_message(self, event):
        message = event['message']
        type = event['mytype']

        # WebSocket으로 메시지 전송
        await self.send(text_data=json.dumps({
            'message': message,
            'type' : type
        }))