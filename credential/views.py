from django.contrib import messages, auth
from django.contrib.admin import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.generic import View


# Create your views here.
# def login_user(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = auth.authenticate(username=username, password=password)
#
#
#         if user is not None:
#             auth.login(request,user)
#             return redirect('/home/')
#             # return render(request,'base.html')
#         else:
#             messages.info(request,"invalid credentials")
#             return redirect('login_user')
#     return render(request,"login.html")

class LoginView(View):
    def get(self, request):
        return render(request, "login.html")

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/home')
        else:
            messages.info(request, 'Invalid credentials')
            return redirect('LoginView')


class RegistrationView(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['password1']
        if password == cpassword:
            if User.objects.filter(username=username).exists():
                messages.info(request, "Username Taken")
                return redirect("RegistrationView")
            elif User.objects.filter(email=email).exists():
                messages.info(request, "Email Taken")
                return redirect("RegistrationView")
            else:
                user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                                email=email, password=password)
                user.save()
                return redirect('LoginView')
        else:
            messages.info(request, "password not matching")
            return redirect("RegistrationView")

        return render(request, 'register.html')


# class LogoutView(View):
#     def get(self, request):
#         return redirect('/home/')

# class LogoutView(View):
#     def get(request):
#         auth.logout(request)
#         return redirect('/home/')

# def register_user(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         first_name = request.POST['first_name']
#         last_name = request.POST['last_name']
#         email = request.POST['email']
#         password = request.POST['password']
#         cpassword = request.POST['password1']
#         if password==cpassword:
#             if User.objects.filter(username=username).exists():
#                 messages.info(request,"Username Taken")
#                 return redirect("register_user")
#             elif User.objects.filter(email=email).exists():
#                 messages.info(request,"Email Taken")
#                 return redirect("register_user")
#             else:
#                 user = User.objects.create_user(username=username,first_name=first_name,last_name=last_name,email=email,password=password)
#                 user.save()
#
#                 return redirect("login_user")
#         else:
#             messages.info(request,"password not matching")
#             return redirect("register_user")
#     return render(request,'register.html')
#
#
#
#
#
# def logout(request):
#     auth.logout(request)
#     return redirect('/home/')
def LogoutView(request):
    auth.logout(request)
    return redirect('/home/')