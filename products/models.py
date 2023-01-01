from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    title = models.CharField(max_length=255, null=False)
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    price = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='products', null=True)
    approved_by = models.ForeignKey(User, related_name="approved_by", null=True, on_delete=models.SET_NULL)
    approved = models.BooleanField(default=False)
    display_on_main_page = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Category(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='category', null=True)

    def __str__(self):
        return self.title


class CategoryProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)

    def __str__(self):
        return self.category.title + '----' + self.product.title
