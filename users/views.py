from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth import authenticate, login ,logout
from django.contrib.auth import get_user_model
from .models import BaseUser
User = get_user_model()

class LoginView(View):
    template_name = "users/log-in.html"

    def get(self, request, *args, **kwargs):
        return render(request,self.template_name)
    
    def post(self, request):
        email = request.POST['email']
        password = request.POST['password']
        print(email,password)
        user = authenticate(email=email, password=password)
        print(user)
        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(request,f'Wellcome {user.email}')
                return redirect('profile')
        else:
            messages.error(request,'Please enter valid Email Id and Password')
            return redirect('login')


class SingupView(View):
    template_name = "users/sign-up.html"

    def get(self, request, *args, **kwargs):
        return render(request,self.template_name)
    
    def post(self, request):
        email = request.POST['email']
        password = request.POST['Password']
        user_type = request.POST['dropdown']
        if user_type == 'user_none':
            messages.success(request, 'Selete User TYpe')
            return redirect('singup')
        if User.objects.filter(email = email).exists():
            messages.error(request,'That username is taken')
            return redirect('singup')
        else:
            user = User.objects.create_user(email = email , password = password,role=user_type)
            user.save()
            messages.success(request, 'You are now registered and can log in')
            return redirect('login')


def logout_view(request):
    logout(request)
    messages.success(request,f'You Are Log Out')
    return redirect('home')
    

class ProfileView(LoginRequiredMixin, View):
    login_url = 'login'
    template_name = "users/profile.html"
    model = BaseUser

    def get(self, request, *args, **kwargs):
        active_user = BaseUser.objects.get(email=request.user.email)
        return render(request,self.template_name,context={'active_user':active_user})

    def post(self, request, *args, **kwargs):
        first_name = request.POST.get('edit_first_name')
        last_name = request.POST.get('edit_last_name')
        birth_date = request.POST.get('edit_birth_date')
        address = request.POST.get('edit_address')

        if request.POST.get('edit_phone') is not None:
            self.model.objects.update(phone_number=request.POST.get('edit_phone'))
        elif request.FILES.get('pic'):
            model = self.model.objects.get(email=request.user)
            model.user_img = request.FILES.get('pic')
            model.save()
        else:
            self.model.objects.update(first_name=first_name,last_name=last_name,birthdate=birth_date,Address=address)

        return redirect('profile')