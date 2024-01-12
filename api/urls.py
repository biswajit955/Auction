from django.urls import reverse,path
from . import views

urlpatterns = [
    path('my_cart_api/',views.MyCartApi.as_view(),name='my_cart_api'),
    path('watchlist/<slug:slug>/',views.WatchlistListAddView.as_view(),name='watchlist'),
    path('add_cart/<slug:slug>/',views.AddCartView.as_view(),name='add_cart'),
    path('user_in_product/<str:slug>/<str:user>/',views.UserInProductView.as_view(),name='user_in_product'),
    path('mark_notification_as_read/',views.mark_notification_as_read,name='mark_notification_as_read'),
    path('notification_count/',views.NotificationsCount.as_view(),name='notification_count'),
]
