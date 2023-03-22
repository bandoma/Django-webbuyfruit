from django.urls import include,path
from webclient import views

urlpatterns = [
    path('', views.index),
    path('shop', views.shop)
]
