from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.safestring import mark_safe
from authapp.models import User


class CustomLoginView(LoginView):
    template_name = 'authapp/login.html'


class RegisterView(TemplateView):
    template_name = 'authapp/register.html'

    def post(self, request, *args, **kwargs):
        try:
            if all(
                (
                    request.POST.get('username'),
                    request.POST.get('password1'),
                    request.POST.get('password2'),
                    request.POST.get('first_name'),
                    request.POST.get('last_name'),
                    request.POST.get('password1') == request.POST.get('password2'),
                    request.POST.get('email')
                )
            ):
                new_user = User.objects.create(
                    username=request.POST.get('username'),
                    first_name=request.POST.get('first_name'),
                    last_name=request.POST.get('last_name'),
                    email=request.POST.get('email'),
                    age=request.POST.get('age') if request.POST.get('age') else 0,
                    avatar=request.FILES.get('avatar')
                )
                new_user.set_password(request.POST.get('password1'))
                new_user.save()
                messages.add_message(request, messages.INFO, 'Регистрация прошла успешно')
                return HttpResponseRedirect(reverse('authapp:login'))
            else:
                messages.add_message(request, messages.WARNING, 'Что-то пошло не так')     
                return HttpResponseRedirect(reverse('authapp:register')) 
        except Exception as exp:
            messages.add_message(
                request, 
                messages.WARNING, 
                mark_safe(f'Регистрация не удалась:<br>{exp}')
            )     
            return HttpResponseRedirect(reverse('authapp:register'))  


class CustomLogoutView(LogoutView):
    pass


class EditView(TemplateView):
    template_name = 'authapp/edit.html'

    def post(self, request, *args, **kwargs):
        if request.POST.get('username'):
            request.user.username = request.POST.get('username')
        if request.POST.get('first_name'):
            request.user.first_name = request.POST.get('first_name')
        if request.POST.get('last_name'):
            request.user.lust_name = request.POST.get('last_name')
        if request.POST.get('age'):
            request.user.age = request.POST.get('age')   
        if request.POST.get('email'):
            request.user.email = request.POST.get('email') 
        if request.FILES.get('avatar'):
            request.user.avatar = request.FILES.get('avatar')  
        
        request.user.save()  
        return HttpResponseRedirect(reverse('authapp:edit'))  
