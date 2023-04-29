from django.shortcuts import render
from django.http import HttpRequest,HttpResponseRedirect,HttpResponse
from product import models
from .models import user,ForgetPassword,Report,Order,Payment,Wishlist
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from datetime import datetime
from django.core.mail import send_mail
from django.db.models import Q
# Create your views here.
def index(request: HttpRequest):
    
    userrrr=None
    cart_products=None
    if request.session.get("Userid"):
        
        userrrr=user.objects.get(id=request.session.get("Userid"))
        cart_products = list(userrrr.cart.cart_product_many_many_set.all())
    return render(request, "webclient/index.html",{'user':userrrr,"cart_products": cart_products})
    
def shop(request: HttpRequest):
    products = models.Product.objects.all()
    userrrr=None
    cart_products=None
    if request.session.get("Userid"):
        userrrr=user.objects.get(id=request.session.get("Userid"))
        cart_products = list(userrrr.cart.cart_product_many_many_set.all())
    return render(request, "webclient/shop.html", {"products": products, 'user':userrrr,"cart_products": cart_products})
def register(request:HttpRequest):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        birthday=request.POST['birthday']
        fullname=request.POST['fullname']
        address=request.POST['Address']
        phone=request.POST['phone']
        userr = user.Add(password=password, email=email,username=username,birthday=birthday,fullname=fullname,Address=address,phone=phone)
        return HttpResponseRedirect('Login')
    return render(request, 'webclient/register.html')
def show_users(request:HttpRequest):
    users = users.objects.all()
    return render(request, 'users.html', {'users': users})
def SignOut(request:HttpRequest):
    del request.session["Userid"]
    return HttpResponseRedirect("Login")
def Login(request: HttpRequest):
    if request.session.get("Userid"):
        return HttpResponseRedirect("index")
    return render(request, "webclient/login.html")
def Check(request: HttpRequest):
    email = request.POST["email"]
    password = request.POST["password"]
    userrr = user.CheckLogin(email, password)
    if userrr is not None:
        request.session['Userid'] = userrr.id
    return HttpResponseRedirect("Login")

def rmvCart(request: HttpRequest):
    if "UserId" in request.session:
        userr = user.objects.get(id=request.session.get("Userid"))
        notice = userr.rmvCart(request.GET["productid"])
    else:
        notice = "Bạn chưa đăng nhập"
    return HttpResponse(notice)
def AddtoCart(request: HttpRequest):
    notice = ""
    if "Userid" in request.session:
        userr = user.objects.get(id=request.session.get("Userid"))
        notice = userr.AddtoCart(request.GET["productid"], request.GET["number"])
        
    else:
        notice = "Bạn chưa đăng nhập"
    return HttpResponse(notice)

def getPreCart(request: HttpRequest):
    userr = user.objects.get(id=request.session.get("Userid"))
    cart_products = list(userr.cart.cart_product_many_many_set.all())
    sum_price = sum([cart_product.product.price * cart_product.number  for cart_product in cart_products])
    
    return render(request, "Webclient/preCart.html", {"cart_products": cart_products, "total_price": sum_price})


def changepassword(request: HttpRequest):
    if request.method == 'POST':
        userrrr=user.objects.get(id=request.session.get("Userid"))
        passwordold=request.POST['passwordold']
        passwordnew=request.POST['newpassword']
        passwordconfirm=request.POST['confirmpassword']
        if passwordold == userrrr.password:
            if passwordnew == passwordconfirm:
                userrrr.password=passwordnew
                userrrr.save()
                return render(request,"webclient/changepassword.html",{"form":'Đổi mật khẩu thành công.'} )
            else:
                return render(request,"webclient/changepassword.html" ,{"form":'Không khớp.'})
        else:
            return render(request,"webclient/changepassword.html", {"form":'Mật khẩu cũ không đúng.'})
    return render(request,"webclient/changepassword.html")

def ForgotPassword(request: HttpRequest):
    if request.session.get("Userid"):
        return HttpResponseRedirect("/webclient/index")
    
    if request.method == "POST":
        email = request.POST['email']
        if user.objects.filter(email=email).first():
            userrr = user.objects.get(email=email)
            from Webcon.settings import EMAIL_HOST_USER
            encode = ForgetPassword.Add(userrr, 1)
            send_mail("Lấy lại mật khẩu", f"Đây là link lấy lại mật khẩu của bạn: link http://127.0.0.1:8000/forgotpassword?encode={encode}", EMAIL_HOST_USER, [email])
        return render(request, "webclient/forgetpassword.html", {"notice" : "Đã gửi email. Vui lòng kiểm tra."})
    if "encode" in request.GET:
        encode = request.GET["encode"]
        record = ForgetPassword.objects.get(encode=encode)
        now = datetime.now().astimezone(record.datetime.tzinfo)
        if record.datetime > now:
            request.session['Userid'] = record.user.id
        else:
            return HttpResponseRedirect("/error")
        # record.delete()
        return render(request, "webclient/changepassword2.html", {"user":user.objects.get(id=request.session.get("Userid"))})
    return render(request, "webclient/forgetpassword.html")
def checkpassword(request: HttpRequest):
    newpassword=request.POST['passwordnew']
    confirmpassword=request.POST['passwordconfirm']
    if newpassword==confirmpassword:
        userrr = user.objects.get(id=request.session.get("Userid"))
        userrr.password=newpassword
        userrr.save()
    else: 
        return render(request,"webclient/changepassword2.html")
    return HttpResponseRedirect("index")
def viewcart(request: HttpRequest):
    if not request.session.get("Userid"):
        return HttpResponseRedirect("/User/login")
    userr = user.objects.get(id=request.session.get("Userid"))
    cart_products = list(userr.cart.cart_product_many_many_set.all())
    products = [cart_product.product for cart_product in cart_products]

    sum_price = sum(cart_product.product.price * cart_product.number for cart_product in cart_products)
    return render(request,'webclient/cart.html', {"user":user.objects.get(id=request.session.get("Userid")), 
                                             "cart_products": cart_products, 
                                             "total_price": sum_price})
def updateCart(request: HttpRequest):
    if "action" in request.POST:
        if request.POST["action"] == "Checkout":
            request.session["check_list"] = request.POST.getlist("productid_check")
            return HttpResponseRedirect("/checkout")
    if not request.session.get("Userid"):
        return HttpResponseRedirect("Login")
    ids = request.POST.getlist("productid")
    number = request.POST.getlist("number")
    userr = user.objects.get(id=request.session.get("Userid"))
    userr.Update(ids, number)
    return HttpResponseRedirect("/cart")

def about(request:HttpRequest):
    userrrr=None
    cart_products=None
    if request.session.get("Userid"):
        userrrr=user.objects.get(id=request.session.get("Userid"))
        cart_products = list(userrrr.cart.cart_product_many_many_set.all())

    return render(request,"webclient/about.html",{'user':userrrr,"cart_products":cart_products})
def Checkout(request: HttpRequest):
    if request.method == "POST":
        name =  request.POST["name"]
        address = request.POST["address"]
        phone = request.POST["phone"]
        productids = request.POST.getlist("product_id")
        numbers = request.POST.getlist("number")
        order = Order.Add(user.objects.get(id=request.session.get("Userid")), name, address, phone, productids, numbers)[1]
        return HttpResponseRedirect(f"/Receipt?payment={order.id}")

    check_list = request.session["check_list"] 
    userr = user.objects.get(id=request.session.get("Userid"))
    Query = None
    for check_id in check_list:
        if Query == None:
            Query = Q(id = check_id) 
        else:
            Query |= Q(id = check_id) 

    cart_products = list(userr.cart.cart_product_many_many_set.filter(Query))
    products = [cart_product.product for cart_product in cart_products]
    sum_price = sum(product.price for product in products)
    return render(request, "webclient/checkout.html", {"user":user.objects.get(id=request.session.get("Userid")), 
                                                  "cart_products": cart_products, 
                                                  "total_price": sum_price})
def receipt(request: HttpRequest,payment=None):
    
    payment=Payment.objects.filter(order_id=request.GET["payment"])
    if not payment.exists():
        # payment = Payment.objects.get(order_id = 3)
        return HttpResponseRedirect("/error")
    payment=payment[0]
    order_details = payment.order.order_detail_set.all()
    order = payment.order

    sum_price = sum([order_detail.product.price * order_detail.number for order_detail in order_details])

    return render(request, "webclient/receipt.html", {"user":user.objects.get(id=request.session.get("Userid")),
                                                 "order_details" : order_details,
                                                 "order": order,
                                                 "total_price" : sum_price})
def contactus(request:HttpRequest):
    userrrr=None
    cart_products=None
    if request.session.get("Userid"):
        userrrr=user.objects.get(id=request.session.get("Userid"))
        cart_products = list(userrrr.cart.cart_product_many_many_set.all())
    return render(request,"webclient/contact-us.html",{'user':userrrr,'cart_products':cart_products})
def gallery(request:HttpRequest):
    userrrr=None
    cart_products=None
    if request.session.get("Userid"):
        userrrr=user.objects.get(id=request.session.get("Userid"))
        cart_products = list(userrrr.cart.cart_product_many_many_set.all())
    return render(request,"webclient/gallery.html",{'user':userrrr,'cart_products':cart_products})
def myaccount(request:HttpRequest):
    userrrr=None
    cart_products=None
    if request.session.get("Userid"):
        userrrr=user.objects.get(id=request.session.get("Userid"))
        cart_products = list(userrrr.cart.cart_product_many_many_set.all())
    return render(request,"webclient/my-account.html",{'cart_products':cart_products})
def wishlist(request: HttpRequest):
    userrrr=None
    cart_products=None
    if not request.session.get("Userid"):
        return HttpResponseRedirect("/Login")
    if request.session.get("Userid"):
        userrrr=user.objects.get(id=request.session.get("Userid"))
        cart_products = list(userrrr.cart.cart_product_many_many_set.all())
    wlist = Wishlist.objects.filter(user = user.objects.get(id=request.session.get("Userid")))
    return render(request, "webclient/wishlist.html", {"user": user.objects.get(id=request.session.get("Userid")),
                                                  "list" : wlist,"cart_products":cart_products })
def AddtoWishList(request: HttpRequest):
    notice = ""
    if "UserId" in request.session:
        userr = user.objects.get(id=request.session.get("Userid"))
        notice = Wishlist.Add(userr, request.GET["productid"])
    else:
        notice = "Bạn chưa đăng nhập"
    return HttpResponse(notice)
def shopdetail(request: HttpRequest,id):
    userrrr=None
    if request.session.get("Userid"):
        userrrr=user.objects.get(id=request.session.get("Userid"))
    productt = models.Product.objects.get(id=id)
    return render(request,"webclient/shop-detail.html",{'user': userrrr,'product': productt})
def report(request:HttpRequest):
    if request.session.get("Userid"):
        if request.method=="POST":
            message = request.POST['message']
            dt = datetime.now()
            userr = user.objects.get(id=request.session.get("Userid"))
            Report.objects.create(message=message, datetime=dt,user=userr)
        return render(request,"webclient/report.html",{"thongbao" : "admin đã nhận tin nhắn của bạn ","cart_products":list(user.cart.cart_product_many_many_set.all()) })
    return render(request,"webclient/report.html")
        






