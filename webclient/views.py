from django.shortcuts import render
from django.http import HttpRequest,HttpResponseRedirect,HttpResponse
from product import models
from .models import user,ForgetPassword,Report,Order,Payment,Wishlist
from product.models import Product
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from datetime import datetime
from django.core.mail import send_mail
from django.db.models import Q,F
from Admin.models import traloiuser
import numpy as np
import hashlib
from datetime import timedelta
# Create your views here.
def index(request: HttpRequest):
    report=Report.objects.all()
    userrrr=None
    cart_products=None
    traloi=None
    if request.session.get("Userid"):
        userrrr=user.objects.get(id=request.session.get("Userid"))
        cart_products = list(userrrr.cart.cart_product_many_many_set.all())
        traloi=traloiuser.objects.filter(user=userrrr)
    return render(request, "webclient/index.html",{'user':userrrr,"cart_products": cart_products,"reports": report,"traloi":traloi})
    
def shop(request: HttpRequest):
    report=Report.objects.all()
    products = models.Product.objects.all()
    userrrr=None
    cart_products=None
    if request.session.get("Userid"):
        userrrr=user.objects.get(id=request.session.get("Userid"))
        cart_products = list(userrrr.cart.cart_product_many_many_set.all())
    return render(request, "webclient/shop.html", {"products": products, 'user':userrrr,"reports": report,"cart_products": cart_products})
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
        passwordold=hashlib.md5(str(passwordold).strip().encode()).hexdigest()
        passwordnew=request.POST['newpassword']
        passwordconfirm=request.POST['confirmpassword']
        if passwordold == userrrr.password:
            if passwordnew == passwordconfirm:
                passwordnew=hashlib.md5(str(passwordnew).strip().encode()).hexdigest()
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
        newpassword=hashlib.md5(str(newpassword).strip().encode()).hexdigest()
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
    sum_price = sum(cart_product.product.price * cart_product.number for cart_product in cart_products )
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
    if not request.session.get("Userid"):
        return HttpResponseRedirect("/Login")
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
    if "Userid" in request.session:
        userr = user.objects.get(id=request.session.get("Userid"))
        notice = Wishlist.Add(userr, request.GET["productid"])
    else:
        notice = "Bạn chưa đăng nhập"
    return HttpResponse(notice)
def shopdetail(request: HttpRequest,id):
    cart_products=None
    userrrr=None
    if request.session.get("Userid"):
        userrrr=user.objects.get(id=request.session.get("Userid"))
        cart_products = list(userrrr.cart.cart_product_many_many_set.all())
    productt = models.Product.objects.get(id=id)
    return render(request,"webclient/shop-detail.html",{'user': userrrr,"cart_products":cart_products,'product': productt})
def report(request:HttpRequest):
    cart_products=None
    userrrr=None
    
    if request.session.get("Userid"):
        userrrr=user.objects.get(id=request.session.get("Userid"))
        cart_products = list(userrrr.cart.cart_product_many_many_set.all())
        if request.method=="POST":
            message = request.POST['message']
            dt = datetime.now()
            userr = user.objects.get(id=request.session.get("Userid"))
            Report.objects.create(message=message, datetime=dt,user=userr)
        return render(request,"webclient/report.html",{"thongbao" : "admin đã nhận tin nhắn của bạn ","cart_products":cart_products,"user":userrrr })
    return render(request,"webclient/report.html")
def admintraloi(request: HttpRequest):
    userrrr=user.objects.get(id=request.session.get("Userid"))
    traloi=traloiuser.objects.filter(user=userrrr)
    return render(request,"webclient/admintraloi.html",{"tralois":traloi,"users":userrrr})
def RecommendedSystem(request: HttpRequest):
    result = []
    if request.GET["type"] == "product":
        productid = int(request.GET["productid"])
        product_view = Product.objects.get(id=productid)
        orders = Order.objects.filter(order_detail__product__id = product_view.id)
        if orders.count() > 1000:
            orders = orders[orders.count()-1000:]
        
        products = list(Product.objects.all())
        rate = {}
        for product in products:
            rate[product.id] = 0
            if product.cate_id == product_view.cate_id:
                rate[product.id] += 4
        for order in orders:
            for order_detail in order.order_detail_set.all():
                rate[order_detail.product.id] += 1
        del rate[product_view.id]
        products.remove(product_view)

        values = -np.array(list(rate.values()))
        indicates = values.argsort()
        for i in indicates:
            if -values[i] > 0 and len(result) < 4:
                result.append(products[i])
        return render(request, "webclient/Ajax/recomendProduct.html", {"products": result})
    if request.GET["type"] == "user":
        if "UserId" in request.session:
            current_user = user.objects.get(id=request.session.get("Userid"))
            users = models.User.objects
            if users.count() > 2:
                users = users.filter(order__time_checkout__gt = datetime.today()-timedelta(days=30)).distinct()[:2]
            else:
                users = users.all()
            users = list(users)
            users.remove(current_user)
            users.append(current_user)
            products = list(Product.objects.all())
            matrix = []
            for user in users:
                sold = {}
                for product in products:
                    sold[product.id] = 0
                for order in user.order_set.all():
                    for order_detail in order.order_detail_set.all():
                        sold[order_detail.product.id] += order_detail.number
                        
                matrix.append(list(sold.values()))
    # Cosine similarity là một kỹ thuật tính toán độ tương đồng giữa hai véc-tơ dựa trên cosin của góc giữa chúng. 
    # Nó thường được sử dụng trong lĩnh vực xử lý ngôn ngữ tự nhiên và khai phá dữ liệu.
    # cosine similarity có thể được sử dụng trong các ứng dụng AI để tính toán độ tương đồng giữa các đối tượng hoặc để xử lý và phân tích dữ liệu. 
            cos_sim = []
            for vector in matrix[:-1]:
                a = matrix[-1]
                cos_sim.append(np.dot(vector, a)/(np.linalg.norm(vector)*np.linalg.norm(a))) 
            vitri = np.argsort(cos_sim)
            
            i = 0
            while len(result) < 4:
                if i< len(vitri):
                    vector = matrix[vitri[i]]
                    for j in range(len(vector)):
                        if len(result) > 4:
                            break
                        if vector[j] > 0:
                            if products[j] not in result :
                                result.append(products[j])
                else:
                    if products[i] not in result :
                        result.append(products[i])
                i+=1
        else:
            products = Product.objects.order_by(F("remain") - F("initAmount"))[:4]
            products = list(products)
        result = products
        return render(request, "webclient/Ajax/recomendProduct.html", {"products": result})
        






