from django.urls import path
from . import views
from .views import Pausepayment

app_name='subscription_app'


urlpatterns=[
    path('index', views.index, name='index'),
    path('auth/settings', views.settings, name='settings'),
    path('join',views.join,name='join'),
    path('checkout',views.checkout,name='checkout'),
    path('success',views.success,name='success'),
    path('canceled',views.canceled,name='canceled'),
    path('pausepayment',views.Pausepayment, name="pausepayment"),
    path('Resumepayment', views.Resumepayment, name='Resumepayment'),
    path('delete',views.delete,name='delete'),
    path('Updatesubscription',views.Updatesubscription,name='Updatesubscription'),



]