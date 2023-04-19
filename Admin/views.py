from django.shortcuts import render
from django.http import HttpRequest, HttpResponseRedirect, JsonResponse, HttpResponse
from Admin.models import admin

from product import models
from webclient.models import user
# Create your views here.
def index(request:HttpRequest):
    if not request.session.get("UserId"):
        return HttpResponseRedirect("Login")
    return allProduct(request)

def Check(request: HttpRequest):
    email = request.POST["email"]
    
    password = request.POST["password"]
    ad = admin.CheckLogin(email, password)
    if ad is not None:
        request.session['UserId'] = ad.id
    return HttpResponseRedirect("Login")

def Login(request: HttpRequest):
    if request.session.get("UserId"):
        return HttpResponseRedirect("index")
    return render(request, "login.html")
def SignOut(request:HttpRequest):
    del request.session["UserId"]
    return HttpResponseRedirect("Login")
def addProduct(request: HttpRequest):
    categories = models.Category.objects.all()
    return render(request, "addProduct.html", {"categories":categories, "ad" :getinfo()})

def allCategory(request: HttpRequest):
    categories = models.Category.objects.all()
    return render(request, "allCategory.html", {"categories":categories, "ad" :getinfo()})

def addCategory(request: HttpRequest):
    if "Add" in request.GET:
        nameCate = request.GET["name"]
        models.Category.Add(nameCate)
    categories = models.Category.objects.all()
    return render(request, "addCategory.html", {"categories":categories,
                                                "ad" :getinfo()
                                                })
def editCategory(request: HttpRequest):
    if "Delete" in request.GET:
        id = request.GET["id"]
        models.Category.Delete(id)
    if "Edit" in request.GET:
        category = models.Category.objects.get(id=request.GET["id"])
        category.name = request.GET["name"]
        category.save(force_update=True)
    categories = models.Category.objects.all()
    return render(request, "editCategory.html", {"categories":categories, "ad" :getinfo()})

def allProduct(request: HttpRequest):
    categories = models.Category.objects.all()
    products = models.Product.objects.all()
    return render(request, "allProduct.html", {"categories":categories, "products":products, "ad" :getinfo()})
def allUser(request: HttpRequest):
    users=models.user.objects.all()
    return render(request,"allUser.html",{"users":users})
def addProduct(request: HttpRequest):
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
    return render(request, "addProduct.html", {"categories":categories, "products":products, "ad" :getinfo()})

def editProduct(request: HttpRequest):
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
    return render(request, "editProduct.html", {"categories":categories, "products":products, "ad" :getinfo()})

#ajax
def getCategory(request: HttpRequest):
    cate_id = request.GET["cate_id"]
    category = models.Category.objects.get(id=cate_id)
    return render(request, "Ajax/category.html", {"category":category, "ad" :getinfo()})
    
def getProduct(request: HttpRequest):
    product_id = request.GET["product_id"]
    product = models.Product.objects.get(id=product_id)
    return render(request, "Ajax/product.html", {"product":product, "imgPath": product.GetPathImg(),"ad" :getinfo()})

def getinfo():
    return admin.objects.all()[0]
def getprofile(request: HttpRequest):
    return render(request,"Base/BaseProfile.html",{"ad" :getinfo()})