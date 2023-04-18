from django.db import models
from django.shortcuts import render, redirect
# Create your models here.from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.core.validators import RegexValidator
import datetime
class user(models.Model):
    id = models.AutoField(primary_key=True)
    password = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    username = models.CharField(max_length=50)
    birthday=models.DateField()
    fullname=models.CharField(max_length=40,null=True)
    Address=models.CharField(max_length=40, null=True)
    phone_regex = RegexValidator(regex='\d*', message="Trường này chỉ dùng cho kiểu số.")
    phone = models.CharField(validators=[phone_regex],max_length=12)
    def CheckLogin(email: str, password: str):
        try:
            userr = user.objects.get(email=email, password=password)
        except:
            userr = None
        return userr
class ForgetPassword(models.Model):
    user = models.ForeignKey(user, on_delete=models.CASCADE)
    datetime = models.DateTimeField()
    encode = models.TextField()

    def Add(user : user, duration : int):
        expiredate = datetime.datetime.now() + datetime.timedelta(hours=duration)
        import hashlib
        encode = hashlib.md5(str(expiredate).strip().encode()).hexdigest()
        ForgetPassword.objects.update_or_create(user=user, defaults={"datetime" : expiredate, "encode": encode})[0]
        return encode
# class ChangePasswordForm(models.Model):
#     old_password = models.ForeignKey(user)
#     new_password = models.CharField(widget=models.PasswordInput())
#     confirm_new_password = models.CharField(widget=models.PasswordInput())

    

