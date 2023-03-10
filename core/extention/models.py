from django.db import models



class Slider(models.Model):
    name=models.CharField(max_length=64)
    mobile_image=models.ImageField()
    pc_image=models.ImageField()
    url = models.URLField(null=True)
    



class Product(models.Model):
    name=models.CharField(max_length=64)
    description = models.TextField()
    product_image=models.ImageField()
    url = models.URLField(null=True)



class Advertisement(models.Model):
    name = models.CharField(max_length=64)
    mobile_image=models.ImageField()
    pc_image=models.ImageField()
    url = models.URLField(null=True)