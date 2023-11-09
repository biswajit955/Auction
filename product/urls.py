from django.urls import reverse,path
from . import views

# app_name = 'users'

urlpatterns = [
    path('',views.HomeView.as_view(),name='home'),
    path('all-product/',views.ProductListView.as_view(),name='all_product'),
    path('product-category/<str:slug>/',views.ProductCategoryListView.as_view(),name='product_category'),
    path('product-details/<slug:slug>/',views.ProductDetailView.as_view(),name='product_details'),
    path('watchlist/<slug:slug>/',views.WatchlistView.as_view(),name='watchlist'),
    path('database_entry/',views.database_entry,name='database_entry')
]