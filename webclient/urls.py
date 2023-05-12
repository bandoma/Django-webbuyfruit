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
    path('AddtoCart', views.AddtoCart),
    path('rmvCart', views.rmvCart),
    path('preCart', views.getPreCart),
    path('about',views.about),
    path('contactus',views.contactus),
    path('gallery',views.gallery),
    path('myaccount',views.myaccount),
    path('wishlist',views.wishlist),
    path('AddtoWishList',views.AddtoWishList),
    path('signout',views.SignOut),
    path('forgotpassword',views.ForgotPassword),
    path('checkpassword',views.checkpassword),
    path('changepassword',views.changepassword),
    path('shopdetail',views.shopdetail),
    path('report',views.report),
    path('shopdetail/<int:id>',views.shopdetail),
    path('updateCart',views.updateCart),
    path('Receipt',views.receipt),
    path('checkout',views.Checkout),
    path('admintraloi',views.admintraloi),
    path('recommend',views.RecommendedSystem),
   
    
    


]
