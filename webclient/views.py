from django.shortcuts import render
from django.http import HttpRequest
from product import models

# Create your views here.
def index(request: HttpRequest):
    return render(request, "webclient/index.html")

def shop(request: HttpRequest):
    products = models.Product.objects.all()
    return render(request, "webclient/shop.html", {"products": products})