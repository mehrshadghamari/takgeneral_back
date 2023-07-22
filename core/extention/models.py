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
    category= models.ForeignKey("product.Category",on_delete=models.CASCADE,null=True,blank=True)
    brand = models.ForeignKey("product.ProductBrand",on_delete=models.CASCADE,null=True,blank=True)
    image = models.ImageField()
    mobile_image = models.ImageField()
    alt = models.CharField(max_length=127)
    url = models.CharField(max_length=64)
    link_url = models.CharField(max_length=257)


class Banner(models.Model):
    category= models.ForeignKey("product.Category",on_delete=models.CASCADE,null=True,blank=True)
    brand = models.ForeignKey("product.ProductBrand",on_delete=models.CASCADE,null=True,blank=True)
    image=models.ImageField()
    alt=models.CharField(max_length=127)
    url= models.CharField(max_length=64)
    link_url=models.CharField(max_length=257)



class Content(models.Model):
    product= models.OneToOneField("product.Product",on_delete=models.CASCADE,null=True,blank=True)
    category= models.OneToOneField("product.Category",on_delete=models.CASCADE,null=True,blank=True)
    brand = models.OneToOneField("product.ProductBrand",on_delete=models.CASCADE,null=True,blank=True)
    url=models.CharField(max_length=128,null=True)
    desc = tinymce_model.HTMLField()
    # desc2 = models.TextField(null=True)


class ContentImage(models.Model):
    content = models.ForeignKey("extention.Content", on_delete=models.CASCADE,null=True,blank=True)
    image= models.ImageField(null=True,blank=True)
    # alt = models.CharField(max_length=127,null=True,blank=True)




class MetaTag(models.Model):
    product= models.OneToOneField("product.Product",on_delete=models.CASCADE,null=True,blank=True)
    category= models.OneToOneField("product.Category",on_delete=models.CASCADE,null=True,blank=True)
    brand = models.OneToOneField("product.ProductBrand",on_delete=models.CASCADE,null=True,blank=True)
    title = models.CharField(max_length=257)
    desc = models.CharField(max_length=257)
    og_title= models.CharField(max_length=257)
    og_desc= models.CharField(max_length=257)
    og_type= models.CharField(max_length=257)
    og_url= models.CharField(max_length=257)
    og_site_name= models.CharField(max_length=257)
    og_image= models.CharField(max_length=257)
    twiter_cart = models.CharField(max_length=257)
    script = models.TextField()
