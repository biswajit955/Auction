from django.urls import reverse,path
from . import views

# app_name = 'users'

urlpatterns = [
    path('',views.HomeView.as_view(),name='home'),
    path('all-product/',views.ProductListView.as_view(),name='all_product'),
    path('product-category/<str:slug>/',views.ProductCategoryListView.as_view(),name='product_category'),
    path('product-details/<slug:slug>/',views.ProductDetailView.as_view(),name='product_details'),
    path('my_watchlist_list/',views.MyWatchlistList.as_view(),name='my_watchlist_list'),
    path('my_bid_list/',views.MyBidList.as_view(),name='my_bid_list'),
    path('my_cart/',views.MyCartList.as_view(),name='my_cart'),
    path('database_entry/',views.database_entry,name='database_entry')
]