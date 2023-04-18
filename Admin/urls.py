
from django.urls import include,path
from Admin import views


urlpatterns = [
    path('index', views.index),
    path('',views.index),
    path('Login', views.Login),
    path('Check', views.Check),
    path('Product', views.allProduct),
    path('addProduct', views.addProduct),
    path('editProduct', views.editProduct),
    path('Category', views.allCategory),
    path('addCategory', views.addCategory), 
    path('editCategory', views.editCategory),
    path('getCategory', views.getCategory),
    path('getProduct', views.getProduct),
    path('profile',views.getprofile),
    path('signout',views.SignOut)
]
