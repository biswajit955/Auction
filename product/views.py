from datetime import datetime
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render ,redirect
from django.views import View
from django.views.generic.list import ListView 
from django.views.generic.detail import DetailView
from product.serializers import WatchlistSerializer
from django.contrib import messages
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import BaseUser
from .models import Product ,Category,Image ,ProductVisit, Watchlist
import requests
import random
from django.core.files.base import ContentFile

def database_entry(request):
    url = 'https://dummyjson.com/products'

    response = requests.get(url)
    response_data = response.json()

    # for product in response_data:
    #     Category.objects.create(title=product)
    i =12
    for product in response_data['products']:
        img_list = []
        for img_url in product['images']:
            response = requests.get(img_url)
            image_content = ContentFile(response.content)
            filename = img_url.split("/")[-1]  # Extracts the filename from the URL
            image = Image.objects.create(image=image_content)
            image.image.name = filename  # Set the name attribute
            image.save()
            img_list.append(image)

        categories, created = Category.objects.get_or_create(title=product['category'])

        random_number = random.randint(int(product['price']) + 2000, int(product['price']) + 4000)
        products = Product.objects.create(
            id = i,
            title=product['title'],
            Description=product['description'][0:149],
            starting_price=product['price'],
            final_price=random_number,
            product_code = i,
            discount_percentage=product['discountPercentage'],
            categories=categories,
            bid_start_time='2023-09-10',
            bid_end_time='2023-09-20',
            current_bid_amount=0,
            active_bidders=0,
            total_bids=0
        )

        last_image = img_list[-1]
        products.thumbnail_image = last_image.image
        products.images.set(img_list)
        products.save()
        i+=1
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


    # def get(self, request, *args, **kwargs):
    #     all_category = Category.objects.all()

    #     all_product = Product.objects.all()
    #     all_product_img =[]
    #     for product in all_product:
    #         all_product_img.append([i.image for i in product.images.all()])
    #     return render(request,self.template_name,context={'all_category':all_category,
    #                                                       'all_product':all_product,
    #                                                       'all_product_img':all_product_img[-1]})

    
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
        product = Product.objects.get(slug=kwargs['slug'])
        if 'exit' in self.request.POST:
            print(request.user)
            product.bider.remove(request.user)
            product.active_bidders = product.bider.count()
            product.save()
            return redirect('all_product')
            
        product.bider.add(request.user)
        product.buyer = request.user
        product.total_bids += 1
        product.active_bidders = product.bider.count()
        product.current_bid_amount = float(datas)
        product.save()
        messages.success(request, 'Your Bid is updated and You are the high Bidder Right.')
        return redirect('product_details', slug=kwargs['slug'])
    



class WatchlistView(APIView):
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