from rest_framework import serializers

from users.models import BaseUser

from .models import Product,Watchlist
from queue import Queue

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

    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     representation['bider_name'] = BaseUser.objects.get(id = representation['buyer']).email
    #     return representation




    