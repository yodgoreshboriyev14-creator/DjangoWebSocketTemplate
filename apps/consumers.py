# apps/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self): # connect  boglash uchun sizdan room_name oladi va group_name yaratadi
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept() # # #

    async def disconnect(self, close_code):  # Qachonki siz site dan chiqsangiz disconnect avtomatik ishlaydi
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):     # receive xabar yuborilsa ishalydi
        data = json.loads(text_data) #  string kirib keladi va loads qilib  dict ga aylantirib olinyapti
        message = data["message"]


        await self.channel_layer.group_send(
            self.room_group_name,
            {"type": "chat_message", "message": message},
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({"message": event["message"]}))


class NotificationsConsumers(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = "notifications"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def notify_message(self, event):
        await self.send(text_data=json.dumps({
            "message": event["message"],
        }))
