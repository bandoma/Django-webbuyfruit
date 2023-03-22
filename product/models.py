from django.db import models
from django.templatetags.static import static

# Create your models here.
class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    def Add(name: str):
        if Category.objects.filter(name=name).count()==0:
            Category.objects.create(name=name)
    def Delete(id: int):
        if Category.objects.filter(id=id).count()!=0:
            Category.objects.filter(id=id).delete()
        

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    cate_id = models.ForeignKey(Category, verbose_name=("cate_id"), on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    price = models.IntegerField()
    initAmount = models.IntegerField()
    remain = models.IntegerField()
    image = models.CharField(max_length=255)

    def Add(name, cate_id, description, price, amount, image):
        category = Category.objects.filter(id=cate_id).get()
        new = Product()
        new.name = name
        new.cate_id = category
        new.description = description
        new.price = price
        new.initAmount = new.remain = amount
        new.image = image
        new.save(True)
    
    def GetPathImg(self):
        return "/static/images/product/"+self.image
