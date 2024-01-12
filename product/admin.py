from django.contrib import admin

from .models import Image, Category, Product, Bid, ProductVisit, CartItem, Watchlist ,Notification


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'image', 'uploaded_at')
    list_filter = ('uploaded_at',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category_images', 'slug')
    search_fields = ('slug',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'slug',
        'Description',
        'starting_price',
        'final_price',
        'featured',
        'thumbnail_image',
        'discount_percentage',
        'status',
        'product_code',
        'categories',
        'seller',
        'buyer',
        'exits',
        'bid_start_time',
        'bid_end_time',
        'current_bid_amount',
        'active_bidders',
        'total_bids',
    )
    list_filter = (
        'featured',
        'status',
        'exits',
        'bid_start_time',
        'bid_end_time',
    )
    search_fields = ('slug',)


@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'bidder',
        'product',
        'bid_amount',
        'created_on',
        'updated_on',
        'created_by',
    )
    list_filter = (
        'bidder',
        'product',
        'created_on',
        'updated_on',
        'created_by',
    )


@admin.register(ProductVisit)
class ProductVisitAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'timestamp')
    list_filter = ('user', 'product', 'timestamp')


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'quantity', 'added_at')
    list_filter = ('user', 'product', 'added_at')


@admin.register(Watchlist)
class WatchlistAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')
    list_filter = ('user',)

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'content', 'is_read', 'created_at')
    list_filter = ('id',)