from django.urls import reverse,path
from . import views

# app_name = 'users'

urlpatterns = [
    path('log_in/',views.LoginView.as_view(),name='login'),
    path('sing_up/',views.SingupView.as_view(),name='singup'),
    path('logout/',views.logout_view,name='logout'),
    
    path('profile/',views.ProfileView.as_view(),name='profile'),
]
