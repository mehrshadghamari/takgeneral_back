from django.db import models



class Slider(models.Model):
    name=models.CharField(max_length=64)
    mobile_image=models.ImageField()
    pc_image=models.ImageField()
    url = models.CharField(max_length=64,null=True)
    



class ProductClassification(models.Model):
    name=models.CharField(max_length=64)
    description = models.TextField()
    product_image=models.ImageField()
    url = models.CharField(max_length=64,null=True)



class Advertisement(models.Model):
    name = models.CharField(max_length=64)
    mobile_image=models.ImageField()
    pc_image=models.ImageField()
    url = models.CharField(max_length=64,null=True)


# class PompMain(models.Model):
    # name=models.CharField(max_length=64)
    # image=models.ImageField()
    # url = models.CharField(max_length=64,null=True)



# class PompType(models.Model):
    # name=models.CharField(max_length=64)
    # image=models.ImageField()
    # url = models.CharField(max_length=64,null=True)


# class PompBrand(models.Model):
    # name=models.CharField(max_length=64)
    # image=models.ImageField()
    # url =models.CharField(max_length=64,null=True)



