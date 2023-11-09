# tasks.py
from celery import shared_task
from .consumers import OnlineUsersConsumer  
import asyncio
from channels.layers import get_channel_layer

@shared_task
def send_active_users_count_periodically():
    room_name = 'demo_product'

    channel_layer = get_channel_layer()

    room_group_name = f"product_detail_{room_name}"
    count =24

    async def send_count():
        await channel_layer.group_send(
            room_group_name,
            {
                'type': 'active_users',
                'count':count
            }
        )

    asyncio.run(send_count())