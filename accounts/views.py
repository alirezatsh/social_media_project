from typing import Any
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render , redirect
from django.contrib import messages
from .forms import UserRegisterForm , USerLoginForm , EditUserProfile
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import login , logout , authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from home.models import Post
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from .models import Relation , Profile


class UserRegisterView(View):
    
    def dispatch(self, request , *args ,**kwargs):
        if request.user.is_authenticated:
            messages.info(request , "User is authenticated")
            return redirect('home_page')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self , request):
        form = UserRegisterForm()
        return render(request , 'accounts/register.html', {'form': form})


    def post(self , request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.create_user(cd['username'], cd['email'] , cd['password1']) 
            user.first_name = cd['first_name']
            user.last_name = cd['last_name']
            # Profile.objects.create(user=user)
            messages.success(request, 'you have registered')
            return redirect('home_page')
        return render(request , 'accounts/register.html', {'form':form})
    
    



class UserLoginView(View):
    
    def dispatch(self, request , *args ,**kwargs):
        if request.user.is_authenticated:
            messages.info(request , 'user is logged in')
            return redirect('home_page')
        return super().dispatch(request, *args, **kwargs)
    def get(self , request):
        form = USerLoginForm()
        return render(request , 'accounts/login.html', {'form' : form})
    
    def post(self , request):
        form = USerLoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request , username = cd['username'] , password = cd['password']) 
            if user is not None:
                login(request, user)
                messages.success(request, 'you have successfully logged in')
                return redirect('home_page')
            messages.error(request, 'username or password incorrect')
        return render(request , 'accounts/login.html' , {'form' : form})
    
    
    
    
class UserLogoutView( LoginRequiredMixin,  View):
    def get(self , request):
        logout(request)
        messages.success(request , 'you have succesfully logged out')
        return redirect('home_page')
    
    
class UserProfileView(LoginRequiredMixin , View):
    def get(self , request , user_id):
        is_following = False
        user = User.objects.get(pk=user_id)
        posts = user.posts_shell.all()
        relation = Relation.objects.filter(from_user=request.user , to_user = user)
        if relation.exists():
            is_following = True
        return render(request , 'accounts/profile.html', {'user' : user , 'posts' : posts , 'is_following' : is_following})
    
    
class UserPasswordResetView(auth_views.PasswordResetView):
    template_name = 'accounts/password_reset_form.html'
    success_url = reverse_lazy('password_reset_done')
    email_template_name = 'accounts/password_reset_email.html'
    
    

class UserPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'


class UserPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')
    
    
class UserPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'
    
    
    
class UserFollowView(LoginRequiredMixin , View):
    def get(self , request, user_id):
        user = User.objects.get(id=user_id)
        relation = Relation.objects.filter(from_user=request.user , to_user = user)
        if relation.exists():
            messages.error(request, 'you have already followed this user')

        else:
            Relation(from_user=request.user, to_user=user).save()
            messages.success(request, 'you have successfully followed this user')
        return redirect('profile_page' , user.id)
    
    
class UserUnfollowView(LoginRequiredMixin , View):
    def get(self , request, user_id):
        user = User.objects.get(id=user_id)
        relation = Relation.objects.filter(from_user=request.user , to_user = user)
        if relation.exists():
            relation.delete()
            messages.success(request , 'you have successfully unfollowed this user')
        else:
            messages.error('you are not following this user')
        return redirect('profile_page' , user.id)
    
    

class UserEditView(LoginRequiredMixin , View):
    form_class = EditUserProfile
    def get(self , request):
        form = self.form_class(instance=request.user.profile , initial={'email': request.user.email})
        return render(request , 'accounts/edit.html', {'form': form})
    def post(self , request):
        form = self.form_class(request.POST , instance=request.user.profile)
        if form.is_valid():
            form.save()
            request.user.email = form.cleaned_data['email']
            request.user.save()
            messages.success(request , 'profile updated successfully')
        return redirect('profile_page' , request.user.id)