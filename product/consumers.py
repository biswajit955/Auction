# consumers.py
from channels.db import database_sync_to_async
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from datetime import datetime
from product.models import Notification, Product
from users.models import BaseUser

class OnlineUsersConsumer(AsyncWebsocketConsumer):
    rooms = {}

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"count_user_{self.room_name}"

        if self.room_group_name not in self.rooms:
            self.rooms[self.room_group_name] = set()

        self.rooms[self.room_group_name].add(self.scope['user'].id)
        count = len(self.rooms[self.room_group_name])

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'active_users',
                'count': count
            }
        )

    async def disconnect(self, close_code):
        if self.room_group_name in self.rooms:
            self.rooms[self.room_group_name].discard(self.scope['user'].id)
            count = len(self.rooms[self.room_group_name])

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'active_users',
                    'count': count
                }
            )

            if not self.rooms[self.room_group_name]:
                del self.rooms[self.room_group_name]

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def active_users(self, event):
        count = event['count']
        await self.send(text_data=str(count))


class BidUpdateConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"product_detail_{self.room_name}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        database_amount = await database_sync_to_async(Product.objects.get)(slug=self.room_name)
        user = await database_sync_to_async(BaseUser.objects.get)(email=data['username'])
        bider_user = await database_sync_to_async(list)(database_amount.bider.all())
        bider_user = [user.email for user in bider_user]
        

        Last_bidder = f"{user.first_name} {user.last_name}"
        if Last_bidder == ' ':
            Last_bidder = f"{user.email}"
        if database_amount.current_bid_amount != None:
            last_bid_increment = float(data['price']) - float(database_amount.current_bid_amount)
        else:
            last_bid_increment = float(data['price'])
            
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type':'send_amount',
                'price':data['price'],
                'last_bid_increment' :last_bid_increment,
                'total_bids' : int(database_amount.total_bids)+1 if database_amount.total_bids else 1,
                'active_bidders':len(bider_user),
                'last_bidder':Last_bidder
                
            }
        )

    async def send_amount(self, event):
        await self.send(text_data=json.dumps(event))


class BidNotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"notification_{self.room_name}"
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        user = self.scope["user"]
        price = text_data_json['price']
        product = text_data_json['product']
        data = await self.create_notification(product, price,user)
        dt_object = datetime.fromisoformat(str(data["notification"].created_at))
        formatted_string = dt_object.strftime("%Y-%m-%d / %H.%M")

        notification_data = {
            'id': data["notification"].id,
            'content': data["notification"].content,
            'created_at': formatted_string,
            'img':str(data["product"].thumbnail_image),
            'slug':data["product"].slug,
        }
        await self.send_bid_notification(notification_data)

    @database_sync_to_async
    def create_notification(self, products, price,user):
        pro = Product.objects.get(slug=products)
        print(pro.current_bid_amount,price)
        content = f" Bid for {pro.title} increased! Place your bid now!"
        all_biders = [i.email for i in pro.bider.all()]
        all_biders.remove(str(user))
        for users in all_biders:
            notification= Notification.objects.create(user=BaseUser.objects.get(email=users),product=pro, content=content)
        return {"notification":notification,"product":pro}

    async def send_bid_notification(self,content):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'notification',
                'content': content
            }
        )


    async def notification(self, event):
        await self.send(text_data=json.dumps(event))