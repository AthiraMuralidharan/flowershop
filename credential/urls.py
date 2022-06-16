from . import views
from django.urls import path
# app_name='credential'
urlpatterns=[
    path('registerview/',views.RegistrationView.as_view(),name='RegistrationView'),
    path('loginview/',views.LoginView.as_view(),name='LoginView'),
    # path('logoutview/',views.LogoutView.as_view(),name='LogoutView'),
    path('logoutview/',views.LogoutView,name='LogoutView'),
]