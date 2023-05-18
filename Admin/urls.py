
from django.urls import include,path,re_path
from Admin import views
# from django.conf.urls import url
from django.conf import settings
from django.views.static import serve

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
    path('signout',views.SignOut),
    path('User',views.allUser),
    path('deleteUser',views.deleteUser),
    path('bieudoduong',views.bieudoduong),
    path('columnchart',views.column_chart),
    path('traloi',views.traloi),
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
]
