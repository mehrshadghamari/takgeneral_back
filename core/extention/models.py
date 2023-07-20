from django.db import models
# from ckeditor.fields import RichTextField
from tinymce import models as tinymce_model


class Slider(models.Model):
    name = models.CharField(max_length=64)
    mobile_image = models.ImageField()
    pc_image = models.ImageField()
    url = models.CharField(max_length=64, null=True)


class ProductClassification(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField()
    product_image = models.ImageField()
    url = models.CharField(max_length=64, null=True)


class Advertisement(models.Model):
    name = models.CharField(max_length=64)
    mobile_image = models.ImageField()
    pc_image = models.ImageField()
    url = models.CharField(max_length=64, null=True)



class MainBanner(models.Model):
    image = models.ImageField()
    mobile_image = models.ImageField()
    alt = models.CharField(max_length=127)
    slug = models.CharField(max_length=64)
    linke_url = models.CharField(max_length=257)


class Banner(models.Model):
    image=models.ImageField()
    alt=models.CharField(max_length=127)
    slug= models.CharField(max_length=64)
    link_url=models.CharField(max_length=257)



class Content(models.Model):
    product= models.ForeignKey("product.Product",on_delete=models.CASCADE,null=True,blank=True)
    url=models.CharField(max_length=128,null=True)
    desc = tinymce_model.HTMLField()


class ContentImage(models.Model):
    content = models.ForeignKey("extention.Content", on_delete=models.CASCADE)
    image= models.ImageField()




# class MetaTag(models.Model):
