from django.db import models
from django_jalali.db import models as jmodels
from product.models import Product
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


class PopularHomeCategory(models.Model):
    category = models.OneToOneField("product.Category", on_delete=models.CASCADE, null=True, blank=True)
    color = models.CharField(max_length=20, null=True, blank=True)
    image = models.ImageField()

    @property
    def products(self):
        if self.category.is_leaf_node():
            product_query = Product.objects.select_related("category").filter(
                category=self.category).order_by('-special_offer')[:20]
        else:
            product_query = Product.objects.select_related("category").filter(
                category__in=self.category.get_children()).order_by('-special_offer')[:20]
        return product_query


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
    title = models.CharField(max_length=257, null=True, blank=True)
    desc = models.CharField(max_length=257, null=True, blank=True)
    og_title = models.CharField(max_length=257, null=True, blank=True)
    og_desc = models.CharField(max_length=257, null=True, blank=True)
    og_locale = models.CharField(max_length=257,default="fa_IR", null=True, blank=True)
    og_type = models.CharField(max_length=257, null=True, blank=True)
    og_url = models.CharField(max_length=257, null=True, blank=True)
    og_site_name = models.CharField(max_length=257,default="tak general", null=True, blank=True)
    og_image = models.CharField(max_length=257, null=True, blank=True)
    twiter_cart = models.CharField(max_length=257, null=True, blank=True)
    canonical = models.CharField(max_length=257, null=True, blank=True)
    follow = models.BooleanField(default=True, null=True, blank=True)
    index = models.BooleanField(default=True, null=True, blank=True)



    @property
    def google_index(self):

        if self.index and self.follow==False:
            return 'index,nofollow'

        if self.index and self.follow==True:
            return 'index,follow'

        if self.index==False and self.follow==False:
            return 'index,nofollow'

        if self.index==False and self.follow==True:
            return 'noindex,follow'

    @property
    def schemas(self):
        return self.schemas.all()


class MetaTagSchema(models.Model):
    meta_tag = models.ForeignKey("extention.MetaTag", related_name='schemas', on_delete=models.CASCADE, null=True,
                                 blank=True)
    schema = models.TextField()
