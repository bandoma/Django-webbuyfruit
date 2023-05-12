from django.shortcuts import render
from django.http import HttpRequest, HttpResponseRedirect, JsonResponse, HttpResponse
from Admin.models import admin

from product import models
from webclient.models import user,Report,Order
from .models import traloiuser
from product.models import Product
import io
import urllib, base64
from django.shortcuts import render
import datetime
import time
from django.http import HttpResponse
# Create your views here.
def index(request:HttpRequest):
    if not request.session.get("UserId"):
        return HttpResponseRedirect("Login")
    report=Report.objects.all()
    users=user.objects.all()
    return render(request,'index.html',{"reports": report,"user":users} )
def Check(request: HttpRequest):
    email = request.POST["email"]
    password = request.POST["password"]
    ad = admin.CheckLogin(email, password)
    if ad is not None:
        request.session['UserId'] = ad.id
    return HttpResponseRedirect("Login")

def Login(request: HttpRequest):
    report=Report.objects.all()
    users=user.objects.all()
    if request.session.get("UserId"):
        return HttpResponseRedirect("index")
    return render(request, "login.html",{"reports": report,"user":users})
def SignOut(request:HttpRequest):
    del request.session["UserId"]
    return HttpResponseRedirect("Login")
def addProduct(request: HttpRequest):
    categories = models.Category.objects.all()
    report=Report.objects.all()
    users=user.objects.all()
    return render(request, "addProduct.html", {"categories":categories, "ad" :getinfo(),"reports": report,"user":users})

def allCategory(request: HttpRequest):
    report=Report.objects.all()
    users=user.objects.all()
    categories = models.Category.objects.all()
    return render(request, "allCategory.html", {"categories":categories,"reports": report,"user":users, "ad" :getinfo()})

def addCategory(request: HttpRequest):
    report=Report.objects.all()
    users=user.objects.all()
    if "Add" in request.GET:
        nameCate = request.GET["name"]
        models.Category.Add(nameCate)
    categories = models.Category.objects.all()
    return render(request, "addCategory.html", {"categories":categories,
                                                "ad" :getinfo(),"reports": report,"user":users
                                                })
def editCategory(request: HttpRequest):
    report=Report.objects.all()
    users=user.objects.all()
    if "Delete" in request.GET:
        id = request.GET["id"]
        models.Category.Delete(id)
    if "Edit" in request.GET:
        category = models.Category.objects.get(id=request.GET["id"])
        category.name = request.GET["name"]
        category.save(force_update=True)
    categories = models.Category.objects.all()
    return render(request, "editCategory.html", {"categories":categories,"reports": report,"user":users, "ad" :getinfo()})

def allProduct(request: HttpRequest):
    report=Report.objects.all()
    users=user.objects.all()
    categories = models.Category.objects.all()
    products = models.Product.objects.all()
    return render(request, "allProduct.html", {"categories":categories,"reports": report,"user":users, "products":products, "ad" :getinfo()})
def allUser(request: HttpRequest):
    report=Report.objects.all()
    users=user.objects.all()
    return render(request,"allUser.html",{"users":users,"ad" :getinfo(),"reports": report,"user":users})
def deleteUser(request: HttpRequest):
    report=Report.objects.all()
    users=user.objects.all()
    if "Delete" in request.GET:
        id = request.GET["id"]
        user.Delete(id)
    return render(request, "deleteUser.html",{"users":users,"ad" :getinfo(),"reports": report,"user":users})
    
def addProduct(request: HttpRequest):
    report=Report.objects.all()
    users=user.objects.all()
    if "Add" in request.GET:
        name = request.GET["name"]
        cate_id = request.GET["cate_id"]
        description = request.GET["description"]
        price = request.GET["price"]
        amount = request.GET["amount"]
        image = request.GET["image"]
        models.Product.Add(name, cate_id, description, price, amount, image)
    categories = models.Category.objects.all()
    products = models.Product.objects.all()
    return render(request, "addProduct.html", {"reports": report,"user":users,"categories":categories, "products":products, "ad" :getinfo()})

def editProduct(request: HttpRequest):
    report=Report.objects.all()
    users=user.objects.all()
    if "Delete" in request.GET:
        models.Product.objects.filter(id=request.GET["id"]).delete()
    if "Edit" in request.GET:
        product = models.Product.objects.get(id=request.GET["id"])
        product.name = request.GET["name"]
        product.cate_id = models.Category.objects.get(name=request.GET["category"])
        product.description = request.GET["description"]
        product.price = request.GET["price"]
        product.remain = request.GET["remain"]
        product.initAmount = request.GET["initAmount"]
        product.image = request.GET["image"]
        product.save(force_update=True)
    categories = models.Category.objects.all()
    products = models.Product.objects.all()
    return render(request, "editProduct.html", {"reports": report,"user":users,"categories":categories, "products":products, "ad" :getinfo()})

#ajax
def getCategory(request: HttpRequest):
    report=Report.objects.all()
    users=user.objects.all()
    cate_id = request.GET["cate_id"]
    category = models.Category.objects.get(id=cate_id)
    return render(request, "Ajax/category.html", {"reports": report,"user":users,"category":category, "ad" :getinfo()})
    
def getProduct(request: HttpRequest):
    report=Report.objects.all()
    users=user.objects.all()
    product_id = request.GET["product_id"]
    product = models.Product.objects.get(id=product_id)
    return render(request, "Ajax/product.html", {"reports": report,"user":users,"product":product, "imgPath": product.GetPathImg(),"ad" :getinfo()})

def getinfo():
    report=Report.objects.all()
    users=user.objects.all()
    return admin.objects.all()[0]
def getprofile(request: HttpRequest):
    report=Report.objects.all()
    users=user.objects.all()
    return render(request,"Base/BaseProfile.html",{"reports": report,"user":users,"ad" :getinfo()})

def bieudoduong(request: HttpRequest):
    report=Report.objects.all()
    users=user.objects.all()
    
    if "type" in request.GET:
        orders=Order.objects.all()
        
        x=[int(time.mktime(order.time_checkout.timetuple())) for order in orders]
        y=[order.totalPrice for order in orders]
        return JsonResponse({"x":x,"y":y,"type":"line"})
    orders=Order.objects.all()
    x=[order.time_checkout.strftime("%d/%m/%Y  %H:%M:%S %p") for order in orders]
    y=[order.totalPrice for order in orders]
    return render(request,"bieudoduong.html",{"reports": report,"user":users,"ad" :getinfo(),"x":x,"y":y,"type":"line"})

def column_chart(request: HttpRequest):
    products = models.Product.objects.all()
    report=Report.objects.all()
    users=user.objects.all()
    x=[product.name for product in products]
    y=[len(product.order_detail_set.all()) for product in products]
    return render(request,"columnchart.html",{"x":x,"y":y,"ad" :getinfo(),"reports": report,"user":users})
def traloi(request: HttpRequest):
    if request.session.get("UserId"):
        if request.method=="POST":
            message = request.POST['message']
            dt = datetime.datetime.now()
            adminn= admin.objects.get(id=request.session.get("UserId"))
            userr=user.objects.get(id=request.POST['userid'])
            traloiuser.objects.create(message=message, datetime=dt,admin=adminn,user=userr)
            return render(request,"senduser.html",{"thongbao" : "Bạn đã gửi tin nhắn cho "+userr.username })
    return render(request,"senduser.html",{"reports":Report.objects.all()})