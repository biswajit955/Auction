from django.utils import timezone
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import gettext_lazy as _
# from languages.fields import LanguageField
from .manager import CustomUserManager
from io import BytesIO
from PIL import Image
from django.core.files import File
import PIL


class BaseUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('seller', 'Seller'),
        ('buyer', 'Buyer'),
    )

    username = None
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    email = models.EmailField(_('email address'), unique=True,
                              error_messages={'unique': _("A user with that email id already exists."),},)
    phone_number = models.CharField(max_length=12,blank=True,null=True)
    birthdate = models.DateField(help_text = "Users birth date",blank=True,null=True)
    Address = models.CharField(help_text = "Users Address",blank=True,null=True,max_length=150)
    user_img = models.ImageField(upload_to='profile_pic',blank=True,null=True)
    # Registration Date
    date_joined = models.DateTimeField(default=timezone.now)

    # Permissions
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
    
    def save(self, *args, **kwargs):
        if self.user_img:
            new_image = self.compress_images(self.user_img)  
            self.user_img = new_image
        super().save(*args, **kwargs)
   

    def valid_extension(self,_img):
        if '.jpg' in _img:
            return "JPEG"
        elif '.jpeg' in _img:
            return "JPEG"
        elif '.png' in _img:
            return "PNG"


    def compress_images(self,image):
        img = Image.open(image)

        if img.height > 300 or img.width > 300:
            new_img = (300, 300)
            img.thumbnail(new_img)
            im_io = BytesIO() 
            img.save(im_io, self.valid_extension(image.name) ,optimize=True, 
            quality=70) 
            new_image = File(im_io, name=image.name)
            return new_image


class Seller(models.Model):
    user = models.OneToOneField(BaseUser, on_delete=models.CASCADE)


class Buyer(models.Model):
    user = models.OneToOneField(BaseUser, on_delete=models.CASCADE)