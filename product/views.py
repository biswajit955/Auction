from datetime import datetime
from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404, render ,redirect
from django.views import View
from django.views.generic.list import ListView 
from django.db.models import F, Q
from product.serializers import AddCartSerializer, CartSerializer, WatchlistSerializer
from django.contrib import messages
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import BaseUser
from .models import CartItem, Product ,Category,Image ,ProductVisit, Watchlist
import requests
import random
from django.core.files.base import ContentFile


def database_entry(request):
    url = 'https://dummyjson.com/products'
    # url = 'https://dummyjson.com/products/categories'


    response = requests.get(url)
    response_data = response.json()

    # for product in response_data:
    #     Category.objects.create(title=product)

    for product in response_data['products']:
        if product['id'] > 20:
            img_list = []
            for img_url in product['images']:
                response = requests.get(img_url)
                image_content = ContentFile(response.content)
                filename = img_url.split("/")[-1]  # Extracts the filename from the URL
                image = Image.objects.create(image=image_content)
                image.image.name = filename  # Set the name attribute
                image.save()
                img_list.append(image)

            # categories, created = Category.objects.get_or_create(title=product['category'])

            # random_number = random.randint(int(product['price']) + 2000, int(product['price']) + 4000)
            # products = Product.objects.create(
            #     title=product['title'],
            #     Description=product['description'][0:149],
            #     starting_price=product['price'],
            #     final_price=random_number,
            #     product_code = random.randint(1,1000),
            #     discount_percentage=product['discountPercentage'],
            #     categories=categories,
            #     bid_start_time='2023-09-10',
            #     bid_end_time='2023-12-20',
            #     current_bid_amount=0,
            #     active_bidders=0,
            #     total_bids=0
            # )
            products = Product.objects.get(title=product['title'])
            last_image = img_list[-1]
            products.thumbnail_image = last_image.image
            products.images.set(img_list)
            products.featured = False
            products.save()
            print(products)
            # products = Product.objects.get(title=product['title'])
            # products.featured = False
            # products.save()


class HomeView(ListView):
    template_name = "product/index.html"
    model = Product

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['all_product'] = self.model.objects.all()
        context['all_category'] = Category.objects.all()
        all_product_img =[]
        for product in self.get_queryset():
            all_product_img.append([i.image for i in product.images.all()])
        context['all_product_img'] = all_product_img[-1]
        context['courent_time']= datetime.now()
        return context

class ProductListView(ListView):
    model = Product
    context_object_name = 'product_list'
    template_name="product/product-list.html"


class ProductCategoryListView(ListView):
    model = Product
    context_object_name = 'product_list'
    template_name="product/product-category-list.html"

    def get_queryset(self, **kwargs):
        qs = super().get_queryset()
        return qs.filter(categories__slug=self.kwargs['slug'])
 

def product_detail(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    if request.user.is_authenticated:
        ProductVisit.objects.get_or_create(user=request.user, product=product)
    return render(request, 'product_detail.html', {'product': product})

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

class ProductDetailView(View):
    model = Product
    template_name="product/product-details.html"

    def get_context_data(self, **kwargs):
        context = {}
        data = get_object_or_404(Product, slug=kwargs['slug'])
        try:
            user = BaseUser.objects.get(email = data.buyer)
            context['user_name'] =f"{user.first_name} {user.last_name}"
        except:
            context['user_name'] =f"No Bidder"

        img = []
        for image in data.images.all():
            img.append(image.image)
        context['product_img'] =img
        context['bid_end'] = data.bid_start_time - data.bid_end_time
        context["product_detail"] = data
        context.update(kwargs)
        return context

    def get(self,request,*args, **kwargs):
        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        datas = request.POST.get('bid_ammount')
        print(datas)
        product = Product.objects.get(slug=kwargs['slug'])
        if 'exit' in self.request.POST:
            print(request.user)
            product.bider.remove(request.user)
            product.active_bidders = product.bider.count()
            product.save()
            return redirect('all_product')
        
        current_bidder = product.buyer
        total_bids = product.total_bids+1 if product.total_bids != None else 1

        product.bider.add(request.user)
        product.buyer = request.user
        product.total_bids = total_bids
        product.active_bidders = product.bider.count()
        product.current_bid_amount = float(datas)
        product.save()
        messages.success(request, 'Your Bid is updated and You are the high Bidder Right.')
        return redirect('product_details', slug=kwargs['slug'])
    

class MyWatchlistList(ListView):
    model = Watchlist
    template_name='product/my-favorites.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if Watchlist.objects.filter(user=self.request.user).exists():
            context["products"] = self.model.objects.get(user=self.request.user).product.all()
            context["active_user"] = BaseUser.objects.get(email=self.request.user.email)
        return context
    

class MyBidList(ListView):
    model = Product
    template_name='product/my-bid.html'
    context_object_name="products"

    def get_queryset(self) -> QuerySet[Any]:
        qs =  super().get_queryset()
        return qs.filter(buyer=self.request.user)
    
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["active_user"] = BaseUser.objects.get(email=self.request.user.email)
        return context
    


class MyCartList(ListView):
    model = CartItem
    template_name='product/my-cart.html'
    context_object_name="products"
    
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        # context["products"] = [p.product for p in self.get_queryset()]
        context["count"] = self.get_queryset().count()
        return context
    



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
            obj =CartItem.objects.get(Q(product=product) & Q(user=request.user))
            data = CartItem.objects.get(Q(product=product) & Q(user=request.user)).delete()
            return Response(({"response":"remove from cart","price":int(obj.product.final_price)*int(obj.quantity)}))