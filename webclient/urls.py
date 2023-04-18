from django.urls import include,path
from webclient import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('index', views.index),
    path('',views.index),
    path('Checkk', views.Check),
    path('shop', views.shop),
    path('Login',views.Login),
    path('register',views.register),
    path('show_users',views.show_users),
    path('cart',views.viewcart),
    path('about',views.about),
    path('checkout',views.checkout),
    path('contactus',views.contactus),
    path('gallery',views.gallery),
    path('myaccount',views.myaccount),
    path('wishlist',views.wishlist),
    path('signout',views.SignOut),
    path('forgotpassword',views.ForgotPassword),
    path('checkpassword',views.checkpassword),
    path('changepassword',views.changepassword),
    path('shopdetail',views.shopdetail),


]
