from django.shortcuts import render
from django.http import HttpRequest,HttpResponseRedirect
from product import models
from .models import user,ForgetPassword
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.messages import constants as messages
import datetime
from django.core.mail import send_mail
# Create your views here.
def index(request: HttpRequest):
    
    userrrr=None
    if request.session.get("Userid"):
        userrrr=user.objects.get(id=request.session.get("Userid"))
    return render(request, "webclient/index.html",{'user':userrrr})
    
def shop(request: HttpRequest):
    products = models.Product.objects.all()
    userrrr=None
    if request.session.get("Userid"):
        userrrr=user.objects.get(id=request.session.get("Userid"))
    return render(request, "webclient/shop.html", {"products": products, 'user':userrrr})
def register(request:HttpRequest):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        birthday=request.POST['birthday']
        fullname=request.POST['fullname']
        address=request.POST['Address']
        phone=request.POST['phone']
        userr = user.objects.create(password=password, email=email,username=username,birthday=birthday,fullname=fullname,Address=address,phone=phone)
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
                return render(request,"webclient/changepassword.html" ,{"form":'Mật khẩu mới và xác nhận mật khẩu không khớp.'})
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
        now = datetime.datetime.now().astimezone(record.datetime.tzinfo)
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
    userrrr=None
    if request.session.get("Userid"):
        userrrr=user.objects.get(id=request.session.get("Userid"))
    return render(request,"webclient/cart.html",{'user':userrrr})
def about(request:HttpRequest):
    userrrr=None
    if request.session.get("Userid"):
        userrrr=user.objects.get(id=request.session.get("Userid"))
    return render(request,"webclient/about.html",{'user':userrrr})
def checkout(request:HttpRequest):
    userrrr=None
    if request.session.get("Userid"):
        userrrr=user.objects.get(id=request.session.get("Userid"))
    return render(request,"webclient/checkout.html",{'user':userrrr})
def contactus(request:HttpRequest):
    userrrr=None
    if request.session.get("Userid"):
        userrrr=user.objects.get(id=request.session.get("Userid"))
    return render(request,"webclient/contact-us.html",{'user':userrrr})
def gallery(request:HttpRequest):
    userrrr=None
    if request.session.get("Userid"):
        userrrr=user.objects.get(id=request.session.get("Userid"))
    return render(request,"webclient/gallery.html",{'user':userrrr})
def myaccount(request:HttpRequest):
    userrrr=None
    if request.session.get("Userid"):
        userrrr=user.objects.get(id=request.session.get("Userid"))
    return render(request,"webclient/my-account.html")
def wishlist(request:HttpRequest):
    userrrr=None
    if request.session.get("Userid"):
        userrrr=user.objects.get(id=request.session.get("Userid"))
    return render(request,"webclient/wishlist.html",{'user':userrrr})
def shopdetail(request: HttpRequest):
    userrrr=None
    if request.session.get("Userid"):
        userrrr=user.objects.get(id=request.session.get("Userid"))
    return render(request,"webclient/shop-detail.html",{'user':userrrr})




