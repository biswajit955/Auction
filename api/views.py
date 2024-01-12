from rest_framework.views import APIView
from api.serializers import AddCartSerializer, CartSerializer, WatchlistSerializer
from product.models import CartItem, Notification, Product ,Category,Image ,ProductVisit, Watchlist
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, render ,redirect
from django.db.models import F, Q
from django.http import JsonResponse



def mark_notification_as_read(request):
    if request.method == 'POST':
        notification_id = request.POST.get('notification_id')
        try:
            notification = Notification.objects.get(id=notification_id)
            notification.is_read = True
            notification.save()
            return JsonResponse({'success': True})
        except Notification.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Notification not found'})

    return JsonResponse({'success': False, 'error': 'Invalid request'})


class MyCartApi(APIView):

    def get(self,request,*args, **kwargs):
        cart_count = CartItem.objects.filter(user=self.request.user).count()
        data = {'cart_count':cart_count}
        return Response(data)
    

class NotificationsCount(APIView):
    def get(self,request,*args, **kwargs):
        notifications = Notification.objects.filter(user=self.request.user)
        count = notifications.filter(is_read=False).count()
        return Response({'notifications_count': count})
    

class WatchlistListAddView(APIView):
    serializer_class = WatchlistSerializer
    def get(self,request,*args, **kwargs):
        user_watchlist = Watchlist.objects.filter(user=request.user).first()
        if user_watchlist:
            serializer = self.serializer_class(user_watchlist)
            return Response(serializer.data)
        else:
            return Response({'watchlist': None}) 

    def post(self, request,slug, *args, **kwargs):
        product = get_object_or_404(Product, slug=slug)
        if request.POST['key']== "select":
            watchlist_instance, created = Watchlist.objects.get_or_create(user=request.user)
            watchlist_instance.product.add(product)
            serializer = self.serializer_class(watchlist_instance)
            return Response(({"response":"Add to Watchlist","data":serializer.data}))
        if request.POST['key']== "remove_select":
            watchlist_instance = Watchlist.objects.get(user=request.user)
            watchlist_instance.product.remove(product)
            serializer = self.serializer_class(watchlist_instance)
            return Response(({"response":"remove from Watchlist","data":serializer.data}))


class AddCartView(APIView):
    serializer_class = CartSerializer
    
    def get(self,request,*args, **kwargs):
        user_cart = CartItem.objects.filter(user=request.user).first()
        if user_cart:
            serializer = AddCartSerializer(user_cart, context={'request': request})
            return Response(serializer.data)
        else:
            return Response({'cart': None})
        
    def post(self, request,slug, *args, **kwargs):
        product = get_object_or_404(Product, slug=slug)
        if request.POST['key']== "add_cart":
            if CartItem.objects.filter(product=product).exists():
                cart_instance = CartItem.objects.get(product=product)
                print(cart_instance.quantity,"..........")
                cart_instance.quantity=cart_instance.quantity+1
                cart_instance.save()
            else:
                cart_instance = CartItem.objects.create(user=request.user,product=product,quantity=1)
            serializer = AddCartSerializer(cart_instance, context={'request': request})
            return Response(({"response":"Add to cart","data":serializer.data}))
        
        if request.POST['key']== "update_cart":
            cart_instance = CartItem.objects.get(Q(product=product) & Q(user=request.user))
            cart_instance.quantity = request.POST['count']
            cart_instance.save()
            return Response(({"response":f"quantity update on {product}"}))

        
        if request.POST['key']== "remove_cart":
            print(product,request.user)
            obj =CartItem.objects.get(Q(product=product) & Q(user=request.user))
            data = CartItem.objects.get(Q(product=product) & Q(user=request.user)).delete()
            return Response(({"response":"remove from cart","price":int(obj.product.final_price)*int(obj.quantity)}))
        


class UserInProductView(APIView):
    def get(self, request,slug,user, *args, **kwargs):
        print(slug,user)
        product = Product.objects.get(slug=slug)
        print([i.email for i in product.bider.all()])
        if str(user) in [i.email for i in product.bider.all()]:
            print("..............")
        if str(user) in [i.email for i in product.bider.all()]:
            return Response(({"response":"Yes"}))
        else:
            return Response(({"response":"No"}))