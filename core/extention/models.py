from django.db import models
# from ckeditor.fields import RichTextField
from tinymce import models as tinymce_model
from django_jalali.db import models as jmodels



class MainBanner(models.Model):
    category = models.ForeignKey("product.Category", on_delete=models.CASCADE, null=True, blank=True,
                                  verbose_name="دسته‌بندی")
    brand = models.ForeignKey("product.ProductBrand", on_delete=models.CASCADE, null=True, blank=True,
                               verbose_name="برند")
    image = models.ImageField(verbose_name="تصویر")
    mobile_image = models.ImageField(verbose_name="تصویر موبایل")
    alt = models.CharField(max_length=127, verbose_name="متن جایگزین")
    url = models.CharField(max_length=64, verbose_name="آدرس")
    link_url = models.CharField(max_length=257, verbose_name="آدرس لینک")

    class Meta:
        verbose_name = "بنر اصلی"
        verbose_name_plural = "بنرهای اصلی"


class Banner(models.Model):
    category = models.ForeignKey("product.Category", on_delete=models.CASCADE, null=True, blank=True,
                                  verbose_name="دسته‌بندی")
    brand = models.ForeignKey("product.ProductBrand", on_delete=models.CASCADE, null=True, blank=True,
                               verbose_name="برند")
    image = models.ImageField(verbose_name="تصویر")
    alt = models.CharField(max_length=127, verbose_name="متن جایگزین")
    url = models.CharField(max_length=64, verbose_name="آدرس")
    link_url = models.CharField(max_length=257, verbose_name="آدرس لینک")

    class Meta:
        verbose_name = "بنر"
        verbose_name_plural = "بنرها"



class Content(models.Model):
    product = models.OneToOneField("product.Product", on_delete=models.CASCADE, null=True, blank=True,
                                    verbose_name="محصول")
    category = models.OneToOneField("product.Category", on_delete=models.CASCADE, null=True, blank=True,
                                     verbose_name="دسته‌بندی")
    brand = models.OneToOneField("product.ProductBrand", on_delete=models.CASCADE, null=True, blank=True,
                                  verbose_name="برند")
    url = models.CharField(max_length=128, null=True, verbose_name="آدرس")
    desc = tinymce_model.HTMLField(verbose_name="توضیحات")

    class Meta:
        verbose_name = "محتوا"
        verbose_name_plural = "محتواها"



class ContentImage(models.Model):
    content = models.ForeignKey("extention.Content", on_delete=models.CASCADE, null=True, blank=True,
                                 verbose_name="محتوا")
    image = models.ImageField(null=True, blank=True, verbose_name="تصویر")

    class Meta:
        verbose_name = "تصویر محتوا"
        verbose_name_plural = "تصاویر محتوا"



class Blog(models.Model):
    title = models.CharField(max_length=257)
    desc = tinymce_model.HTMLField()
    create_time = jmodels.jDateTimeField(auto_now_add=True)    



class MetaTag(models.Model):
    product = models.OneToOneField("product.Product", on_delete=models.CASCADE, null=True, blank=True,
                                   verbose_name="محصول")
    category = models.OneToOneField("product.Category", on_delete=models.CASCADE, null=True, blank=True,
                                    verbose_name="دسته‌بندی")
    brand = models.OneToOneField("product.ProductBrand", on_delete=models.CASCADE, null=True, blank=True,
                                 verbose_name="برند")
    title = models.CharField(max_length=257, verbose_name="عنوان")
    desc = models.CharField(max_length=257, verbose_name="توضیحات")
    og_title = models.CharField(max_length=257, verbose_name="عنوان Open Graph")
    og_desc = models.CharField(max_length=257, verbose_name="توضیحات Open Graph")
    og_type = models.CharField(max_length=257, verbose_name="نوع Open Graph")
    og_url = models.CharField(max_length=257, verbose_name="آدرس Open Graph")
    og_site_name = models.CharField(max_length=257, verbose_name="نام سایت Open Graph")
    og_image = models.CharField(max_length=257, verbose_name="تصویر Open Graph")
    twiter_cart = models.CharField(max_length=257, verbose_name="کارت Twiter")
    script = models.TextField(verbose_name="اسکریپت")

    class Meta:
        verbose_name = "متا تگ"
        verbose_name_plural = "متا تگ‌ها"



