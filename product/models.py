import random
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from users.models import BaseUser
from autoslug import AutoSlugField
from io import BytesIO
from PIL import Image
from PIL import Image as PILImage
from django.core.files.base import ContentFile
from random import randint
from django.utils import timezone


class Image(models.Model):
    image = models.ImageField(upload_to='product_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    # def save(self, *args, **kwargs):
    #     super(Image, self).save(*args, **kwargs)
    #     if self.image:
    #         imag = PILImage.open(self.image.path)  # Use the PILImage class
    #         if imag.width > 400 or imag.height > 300:
    #             output_size = (400, 300)
    #             imag.thumbnail(output_size)
    #             imag.save(self.image.path)


class Category(models.Model):
    title = models.CharField(_('Category Titel'),max_length=225)
    category_images = models.ImageField(upload_to='category_images/',null=True,blank=True)
    slug = AutoSlugField(populate_from='title')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})

    @property
    def get_products(self):
         return Product.objects.filter(categories__title=self.title)


class Product(models.Model):
    title = models.CharField(_('Product Titel'), max_length=150)
    slug = AutoSlugField(populate_from='title')
    Description =  models.CharField(_('Product Description'), max_length=150)
    starting_price = models.DecimalField(max_digits=10,decimal_places=2, null=True,blank=True)
    final_price = models.DecimalField(max_digits=10, decimal_places=2,blank=True)
    featured = models.BooleanField(default=True,null=True,blank=True)
    thumbnail_image = models.ImageField(upload_to='thumbnail_image/',blank=True)
    discount_percentage = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    status = models.BooleanField(default=True,null=True,blank=True)
    product_code = models.CharField(max_length=15,unique=True,blank=True)
    categories = models.ForeignKey(Category, related_name='Category', blank=True,null=True, on_delete=models.CASCADE)
    seller = models.ForeignKey(BaseUser,on_delete=models.CASCADE,null=True,blank=True,related_name="seller_user")
    buyer = models.ForeignKey(BaseUser,on_delete=models.CASCADE,null=True,blank=True,related_name="buyer_user")
    bider = models.ManyToManyField(BaseUser,blank=True,related_name="bider_user")
    images = models.ManyToManyField(Image,blank=True)
    exits = models.BooleanField(default=False,null=True,blank=True)
    bid_start_time = models.DateTimeField()
    bid_end_time = models.DateTimeField()
    current_bid_amount = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    active_bidders = models.IntegerField(null=True,blank=True)
    total_bids = models.IntegerField(null=True,blank=True)

    def valid_extension(self,_img):
        if '.jpg' in _img:
            return "JPEG"
        elif '.jpeg' in _img:
            return "JPEG"
        elif '.png' in _img:
            return "PNG"
    
    def get_thumbnail_upload_path(self, filename):
        category_name = self.categories.name if self.categories else 'default'
        return f'thumbnail_image/{category_name}/{filename}'
    
    @property
    def get_bider(self):
        return self.bider
        # return [BaseUser.objects.filter(id = user) for user in self.bider ]

        
    def save(self, *args, **kwargs):
        super(Product, self).save(*args, **kwargs)
        
        if self.thumbnail_image:
            self.thumbnail_image.upload_to = self.get_thumbnail_upload_path
        
        if not self.product_code: 
            self.product_code = f'SB{random.randint(1000, 9999)}-{random.randint(1000, 9999)}'
            while Product.objects.filter(product_code=self.product_code).exists():
                self.product_code = f'SB{random.randint(1000, 9999)}-{random.randint(1000, 9999)}'

        # if self.thumbnail_image:
        #     pil_image = PILImage.open(self.thumbnail_image.path)
        #     resized_image = pil_image.resize((300, 300), PILImage.LANCZOS)
        #     buffer = BytesIO()
        #     resized_image.save(buffer, format='JPEG')
        #     content = ContentFile(buffer.getvalue())
        #     self.thumbnail_image.save(self.thumbnail_image.name, content, save=False)
        #     buffer.close()
        super(Product, self).save(*args, **kwargs)
        

    def get_absolute_url(self):
        return reverse('product_details', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title


class Bid(models.Model):
    bidder = models.ForeignKey(BaseUser, on_delete=models.SET_NULL ,related_name="bids",null=True)
    product = models.ForeignKey(Product,on_delete=models.SET_NULL ,related_name="product",null=True)
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(BaseUser, on_delete=models.CASCADE, related_name = "bid_createdby", null=True, blank=True)

    def __str__(self):
        return f'{self.bidder.email}-{self.product.title}'
    

class ProductVisit(models.Model):
    user = models.ForeignKey(BaseUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Replace 'Product' with your actual model
    timestamp = models.DateTimeField(default=timezone.now)


class CartItem(models.Model):
    user = models.ForeignKey(BaseUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return self.product.slug
    

class Watchlist(models.Model):
    user = models.ForeignKey(BaseUser, on_delete=models.CASCADE)
    product = models.ManyToManyField(Product,related_name='fav_product')


class Notification(models.Model):
    user = models.ForeignKey(BaseUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='notification_product',null=True,blank=True)
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)  
    
    # def __str__(self):
    #     return self.user.username
