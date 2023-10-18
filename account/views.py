from django.shortcuts import render, redirect
from django.views import View
from .forms import UserRegistrationForm, UserLoginForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

class UserRegisterView(View):

    form_class = UserRegistrationForm
    template_name = 'account/register.html'
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request,*args, **kwargs)
    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form':form})
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(cd['username'], cd['email'], cd['password2'])
            messages.success(request, 'done', 'success')
            return redirect('home:home')
        return render(request, self.template_name, {'form': form})

class UserLoginView(View):
    form_class = UserLoginForm
    template_name = 'account/login.html'
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)
    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form':form})
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request,'loged in', 'success')
                return redirect('home:home')
            messages.error(request, 'wrong password or username', 'danger')
        return render(request, self.template_name, {'form':form})

class UserLogoutView(LoginRequiredMixin, View):

    def get(self, request):
        logout(request)
        messages.success(request,'loged out', 'success')
        return redirect('home:home')
class UserProfileView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = User.objects.get(pk=user_id)
        return render(request, 'account/profile.html', {'user':user})