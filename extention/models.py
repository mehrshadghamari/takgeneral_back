from django.db import models
from django_jalali.db import models as jmodels
from tinymce import models as tinymce_model


class MainBanner(models.Model):
    category = models.ForeignKey("product.Category", on_delete=models.CASCADE, null=True, blank=True)
    brand = models.ForeignKey("product.ProductBrand", on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField()
    mobile_image = models.ImageField()
    alt = models.CharField(max_length=127)
    url = models.CharField(max_length=64)
    link_url = models.CharField(max_length=257)


class Banner(models.Model):
    category = models.ForeignKey("product.Category", on_delete=models.CASCADE, null=True, blank=True)
    brand = models.ForeignKey("product.ProductBrand", on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField()
    alt = models.CharField(max_length=127)
    url = models.CharField(max_length=64)
    link_url = models.CharField(max_length=257)


class HomeMainBanner(models.Model):
    image = models.ImageField()
    mobile_image = models.ImageField()
    alt = models.CharField(max_length=127)
    url = models.CharField(max_length=64)
    link_url = models.CharField(max_length=257)


class HomeBanner(models.Model):
    banner_place = (
        ("mid", "mid"),
        ("end", "end")
    )

    image = models.ImageField()
    alt = models.CharField(max_length=127)
    url = models.CharField(max_length=64)
    link_url = models.CharField(max_length=257)
    place = models.CharField(max_length=5, choices=banner_place, null=True)


class Content(models.Model):
    product = models.OneToOneField("product.Product", on_delete=models.CASCADE, null=True, blank=True)
    category = models.OneToOneField("product.Category", on_delete=models.CASCADE, null=True, blank=True)
    brand = models.OneToOneField("product.ProductBrand", on_delete=models.CASCADE, null=True, blank=True)
    url = models.CharField(max_length=128, null=True)
    desc = tinymce_model.HTMLField()
    # desc2 = models.TextField(null=True)


class ContentImage(models.Model):
    content = models.ForeignKey("extention.Content", on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    # alt = models.CharField(max_length=127,null=True,blank=True)


class Blog(models.Model):
    title = models.CharField(max_length=257)
    desc = tinymce_model.HTMLField()
    tag = models.ManyToManyField("extention.BlogTag")
    slug = models.CharField(max_length=127, null=True)
    created_time = jmodels.jDateTimeField(auto_now_add=True)

    @property
    def blog_images(self):
        return self.blogimage_set.all()

    @property
    def main_image(self):
        return self.blogimage_set.filter(is_main=True).first()

    def __str__(self):
        return self.title


class BlogImage(models.Model):
    blog = models.ForeignKey("extention.Blog", on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    is_main = models.BooleanField(default=False)


class BlogTag(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class MetaTag(models.Model):
    product = models.OneToOneField("product.Product", on_delete=models.CASCADE, null=True, blank=True)
    category = models.OneToOneField("product.Category", on_delete=models.CASCADE, null=True, blank=True)
    brand = models.OneToOneField("product.ProductBrand", on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=257)
    desc = models.CharField(max_length=257)
    og_title = models.CharField(max_length=257)
    og_desc = models.CharField(max_length=257)
    og_type = models.CharField(max_length=257)
    og_url = models.CharField(max_length=257)
    og_site_name = models.CharField(max_length=257)
    og_image = models.CharField(max_length=257)
    twiter_cart = models.CharField(max_length=257)
    script = models.TextField()
