from django.urls import path
from .consumers import *

websocket_urlpatterns = [
    path("ws/online_users/<str:room_name>/", OnlineUsersConsumer.as_asgi()),
    path("ws/update_bid/<str:room_name>/", BidUpdateConsumer.as_asgi()),

]