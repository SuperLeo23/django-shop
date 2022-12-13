from django.urls import path
from . import views

# URL's after playground/
urlpatterns = [
    path('', views.index),
    path('index', views.index),
    path('login/', views.login),
    path('logout/', views.logout),
    path('receipt/', views.receipt),
    path('loginAPI/', views.loginAPI),
    path('cartAPI/', views.addToCart),
    path('panel/', views.panel),
    path('checkout/', views.checkout),
    path('pay/', views.pay),
    path('product/', views.item),
    path('logout/', views.logout)
]