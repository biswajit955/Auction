from rest_framework import serializers

from users.models import BaseUser

from .models import CartItem, Product,Watchlist
from queue import Queue


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = BaseUser
        fields = ('__all__')

class WatchlistSerializer(serializers.ModelSerializer):

    user = serializers.EmailField(source='user.email', read_only=True)
    product = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='slug'
    )

    class Meta:
        model = Watchlist
        fields = ('user', 'product')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return  representation



# class CartSerializer(serializers.ModelSerializer):
#     # user = serializers.EmailField()
#     # product = serializers.SlugRelatedField(
#     #     many=True,
#     #     read_only=True,
#     #     slug_field='slug'
#     # )

#     class Meta:
#         model = CartItem
#         fields = ('user')

#     # Use this method for the custom field
#     def _user(self):
#         request = self.context.get('request', None)
#         print(request.user,"..........")
#         if request:
#             return request.user

#     # def to_representation(self, instance):
#     #     representation = super().to_representation(instance)
#     #     return  representation
    

#     def to_representation(self, instance):
#         representation = super().to_representation(instance)
#         user = self.instance
#         representation['user'] = self._user()
#         return representation
    
class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ('__all__')


class AddCartSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    products = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ('user_email', 'products', 'quantity', 'added_at')

    def get_products(self, obj):
        return [item.product.slug for item in obj.user.cartitem_set.all()]
        



