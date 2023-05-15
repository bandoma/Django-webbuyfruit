from django.db import models
from django.shortcuts import render, redirect
# Create your models here.from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.core.validators import RegexValidator
import datetime
from product.models import Product
import hashlib
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
        password=hashlib.md5(str(password).strip().encode()).hexdigest()
        try:
            userr = user.objects.get(email=email, password=password)
        except:
            userr = None
        return userr
    def Delete(id: int):
        if user.objects.filter(id=id).count()!=0:
            user.objects.filter(id=id).delete()
    def Add(username: str, email: str, password: str,birthday: datetime.datetime,fullname:str,Address:str,phone:str):
        password=hashlib.md5(str(password).strip().encode()).hexdigest()
        userr = user(username=username, email=email, password=password,birthday=birthday,fullname=fullname,Address=Address,phone=phone)
        
        if user.objects.filter(email=email, password=password).exists():
            raise Exception(f"{email} have been used.")  
        else:
            userr.save(force_insert=True)
            Cart.objects.create(userr=userr)

    def AddtoCart(self, product_id: int,number = 1):
        self.cart : Cart
        i = self.cart.Add(product_id,number)
        if type(i) == str:
            return i
        if i>0:
            return "Đã thêm thành công."
        else:
            return "Không thể thêm."
        
    def rmvCart(self, product_id: int):
        self.cart : Cart
        i = self.cart.Remove(product_id)
        if type(i) == str:
            return i
        if i>0:
            return "Đã xoá thành công."
        else:
            return "Không thể xoá."
    def Update(self, productids, numbers):
        self.cart.Update(productids, numbers)
class Cart(models.Model):
    userr = models.OneToOneField(user, on_delete=models.CASCADE, primary_key=True)
    
    def Add(self, product_id: int,number:int):
        try:
            product = Product.objects.get(id = product_id)
            if self.cart_product_many_many_set.filter(product=product).exists():
                return "Đã có sản phẩm."
            cart_product_ = Cart_Product_Many_Many()
            cart_product_.cart_user = self
            cart_product_.number = number
            cart_product_.product = Product(id=product_id)
            cart_product_.AddtoCartTime = datetime.datetime.now()
            cart_product_.save()
        except NameError:
            print(NameError)
            return 0
        return 1
    
    def Remove(self, product_id: int):
        try:
            product = Product.objects.get(id = product_id)
            self.cart_product_many_many_set.filter(product=product).delete()
        except NameError:
            print(NameError)
            return 0
        return 1
    def Update(self, productids, numbers):
        for i in range(len(productids)):
            product = Product.objects.get(id = productids[i])
            cart_detail = self.cart_product_many_many_set.get(product=product)
            cart_detail : Cart_Product_Many_Many
            cart_detail.update(numbers[i])

class Cart_Product_Many_Many(models.Model):
    cart_user = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    AddtoCartTime = models.DateTimeField(auto_now=True)
    number = models.IntegerField(default=1)
    def update(self, number):
        self.number = number
        self.save(force_update=True)
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

class Report(models.Model):
    user=models.ForeignKey(user,on_delete=models.CASCADE)
    message=models.CharField(max_length=255)
    datetime=models.DateTimeField()

# class ChangePasswordForm(models.Model):
#     old_password = models.ForeignKey(user)
#     new_password = models.CharField(widget=models.PasswordInput())
#     confirm_new_password = models.CharField(widget=models.PasswordInput())


class Order(models.Model):
    order_account = models.ForeignKey(user, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=255)
    time_checkout = models.DateTimeField()
    phone = models.CharField(validators=[RegexValidator(regex=r'^\d*$', message="Trường này chỉ dùng cho kiểu số.")],
                             max_length=12)
    show = models.BooleanField(default=True)
    @property
    def totalPrice(self):
            price = [order_detail.price for order_detail in self.order_detail_set.all()]
            if len(price) != 0:
                price = sum(price)
            else:
                price = 0
            return price
    def Add(ordering_account, name, address, phone, productids, amounts):
        order = Order()
        order.order_account = ordering_account
        order.name = name
        order.address = address
        order.time_checkout = datetime.datetime.now()
        order.phone = phone
        order.show = True
        order.save(force_insert=True)
        Payment.Add(order)
        for i in range(len(productids)):
            product = Product.objects.filter(id=productids[i])
            if product.exists():
                Order_detail.Add(order, product[0], amounts[i])
        return "Đặt hàng thành công", order
    
    def getPayment(self):
        return self.payment

class Order_detail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    number = models.IntegerField()
    
    @property
    def price(self):
        return self.number * self.product.price
    
    def Add(order : Order, product : Product, number : int):
        order_detail = Order_detail()
        order_detail.order = order
        order_detail.product = product
        order_detail.number = int(number)
        order_detail.product.remain -= int(number)
        order_detail.product.save(force_update=True)
        order_detail.save(force_insert=True)

class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.DO_NOTHING, primary_key=True)

    def Add(order : Order):
        Payment.objects.create(order = order)
class Wishlist(models.Model):
    user = models.ForeignKey(user, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def Add(user : user, productid):
        if Wishlist.objects.filter(user = user, product= Product.objects.get(id = productid)).exists():
            Wishlist.objects.filter(user = user, product= Product.objects.get(id = productid)).delete()
            return "Đã bỏ yêu thích."
        else:
            wishlist = Wishlist()
            wishlist.product = Product.objects.get(id = productid)
            wishlist.user = user
            wishlist.save(force_insert=True)
            return "Đã thêm yêu thích."
class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    message = models.CharField(max_length=1000)
    user = models.ForeignKey(user, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now=True)

    def Add(productid : int, message : str, userid : int):
        comment = Comment.objects.create(product=Product.objects.get(id=productid), 
                               message=message, 
                               user=user.objects.get(id=userid))
        return "Bình luận thành công"

