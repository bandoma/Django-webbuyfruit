from django.db import models
from django import forms
from django.core.validators import RegexValidator
from webclient.models import user
# Create your models here.
class admin(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField()
    password = models.CharField(max_length=12)
    username = models.CharField(max_length=30)
    fullname=models.CharField(max_length=40,null=True)
    Address=models.CharField(max_length=40, null=True)
    phone_regex = RegexValidator(regex='\d*', message="Trường này chỉ dùng cho kiểu số.")
    phone = models.CharField(validators=[phone_regex],max_length=12)

    def CheckLogin(email: str, password: str):
        try:
            user = admin.objects.get(email=email, password=password)
        except:
            user = None
        return user
class NotifyMessage(models.Model):
    id = models.AutoField(primary_key=True)
    message=models.CharField(max_length=40)
    # iduser=models.ForeignKey("auth_user", on_delete=models.CASCADE)
class traloiuser(models.Model):
    admin=models.ForeignKey(admin,on_delete=models.CASCADE)
    message=models.CharField(max_length=255)
    datetime=models.DateTimeField()
    user=models.ForeignKey(user,on_delete=models.CASCADE,null=True,default=None)
    

