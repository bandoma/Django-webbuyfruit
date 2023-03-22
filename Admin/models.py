from django.db import models
from django import forms
from django.core.validators import RegexValidator
# Create your models here.
class admin(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField()
    password = models.CharField(max_length=12)
    username = models.CharField(max_length=30)

    phone_regex = RegexValidator(regex='\d*', message="Trường này chỉ dùng cho kiểu số.")
    phone = models.CharField(validators=[phone_regex],max_length=12)

    def CheckLogin(email: str, password: str):
        try:
            user = admin.objects.get(email=email, password=password)
        except:
            user = None
        return user
