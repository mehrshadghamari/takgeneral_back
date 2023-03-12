from django.db import models



class Slider(models.Model):
    title=models.CharField(max_length=64)
    mobile_image=models.ImageField()
    pc_image=models.ImageField()
    url = models.CharField(max_length=64,null=True)
    



class Product(models.Model):
    title=models.CharField(max_length=64)
    description = models.TextField()
    image=models.ImageField()
    url = models.CharField(max_length=64,null=True)



class Advertisement(models.Model):
    title = models.CharField(max_length=64)
    mobile_image=models.ImageField()
    pc_image=models.ImageField()
    url = models.CharField(max_length=64,null=True)


class PompMain(models.Model):
    title=models.CharField(max_length=64)
    image=models.ImageField()
    url = models.CharField(max_length=64,null=True)



class PompType(models.Model):
    title=models.CharField(max_length=64)
    image=models.ImageField()
    url = models.CharField(max_length=64,null=True)


class PompBrand(models.Model):
    title=models.CharField(max_length=64)
    image=models.CharField(max_length=64)
    url =models.CharField(max_length=64,null=True)



