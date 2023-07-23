from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import F
from mptt.models import MPTTModel
from mptt.models import TreeForeignKey
from PIL import Image as PilImage


class ProductImage(models.Model):
    image = models.ImageField()
    product = models.ForeignKey(
        'product.Product', on_delete=models.CASCADE, related_name='images')
    alt_text = models.CharField(max_length=255,null=True)
    is_main = models.BooleanField(default=False,)
    created_at = models.DateTimeField(auto_now_add=True,editable=False,null=True)
    upload_at = models.DateTimeField(auto_now=True,null=True)


    # def save(self, *args, **kwargs):

        # super().save()
        # img = PilImage.open(self.original_image)

        # # Resize image for small size
        # small_size = IMAGE_SIZE.get("small", (100, 100))
        # small_img = img.copy()
        # small_img.thumbnail(small_size)
        # small_img_io = BytesIO()
        # small_img.save(small_img_io, format="PNG")
        # small_img_file = InMemoryUploadedFile(small_img_io, None, f"{self.original_image.name.split('.')[:-1]}_small.png", "image/png", small_img_io.tell(), None)
        # self.small_image = small_img_file

        # # Resize image for medium size
        # medium_size = IMAGE_SIZE.get("medium", (300, 300))
        # medium_img = img.copy()
        # medium_img.thumbnail(medium_size)
        # medium_img_io = BytesIO()
        # medium_img.save(medium_img_io, format="PNG")
        # medium_img_file = InMemoryUploadedFile(medium_img_io, None, f"{self.original_image.name.split('.')[:-1]}_medium.png", "image/png", medium_img_io.tell(), None)
        # self.medium_image = medium_img_file

        # # Resize image for large size
        # large_size = IMAGE_SIZE.get("large", (800, 800))
        # large_img = img.copy()
        # large_img.thumbnail(large_size)
        # large_img_io = BytesIO()
        # large_img.save(large_img_io, format="PNG")
        # large_img_file = InMemoryUploadedFile(large_img_io, None, f"{self.original_image.name.split('.')[:-1]}_large.png", "image/png", large_img_io.tell(), None)
        # self.large_image = large_img_file

        # super().save(*args, **kwargs)


class ProductBrand(models.Model):
    name = models.CharField(max_length=64)
    logo = models.ImageField(null=True) #new
    url = models.CharField(max_length=64,null=True,unique=True) # indexing


    def __str__(self):
        return self.name


class ProductManager(models.Manager):
    def with_final_price(self):
        return self.annotate(final_price_Manager=F('price')-(F('price')*F('discount')/100))


class Product(models.Model):
    product_type = models.ForeignKey("product.ProductType",null=True, on_delete=models.RESTRICT)
    category= models.ForeignKey("product.Category",on_delete=models.RESTRICT,null=True)
    slug=models.SlugField(max_length=255,unique=True,null=True)
    name = models.CharField(max_length=64)
    brand = models.ForeignKey('product.ProductBrand', on_delete=models.CASCADE)
    count_of_product = models.IntegerField(default=1)
    discount = models.IntegerField(
        default=0, validators=[MaxValueValidator(99), MinValueValidator(0)])
    price = models.FloatField()
    special_offer = models.BooleanField(default=False)
    seven_days_back = models.BooleanField(default=False)
    free_send = models.BooleanField(default=True)
    waranty_tamir = models.BooleanField()
    waranty_taviz = models.BooleanField()
    month_of_waranty = models.IntegerField()
    created_at = models.DateField(auto_now_add=True, null=True)

    objects = ProductManager()

    @property
    def attributes(self):
        return self.productspecificationvalue_set.all()

    @property
    def main_image (self):
        return self.images.filter(is_main=True).first()
        # if not main_image:
            # main_image = self.images.all().first()
        # return main_image

    @property
    def all_images(self):
        return self.images.all()



    # def similar_product(self):
    #     return self.filter(
    #         price__lte=self.price + 1000000,
    #         price__gte=self.price - 1000000,
    #         category=self.category
    #     ).distinct()[:10]

    @property
    def final_price(self):
        if self.discount == 0:
            return self.price
        return int(self.price - self.price*(self.discount/100))

    @property
    def product_available(self):
        if self.count_of_product == 0:
            return False
        return True

    @property
    def warranty(self):
        if self.waranty_tamir == False and self.waranty_taviz == False:
            return ''

        elif self.waranty_taviz == False:
            return f'{self.month_of_waranty} ماه گارانتی تعمیر '

        elif self.waranty_tamir == False:
            return f'{self.month_of_waranty} ماه گارانتی تعویض '

        elif self.waranty_taviz == True and self.waranty_tamir == True:
            return f' {self.month_of_waranty} ماه گارانتی تعویض و تعمیر '

    def __str__(self):
        return f'id : {self.id} -- name : {self.name} '


# for release 2

class Category(MPTTModel):
    name= models.CharField(max_length=255,unique=True)
    slug=models.SlugField(max_length=255,unique=True)
    image=models.ImageField(null=True,blank=True)
    alt_text= models.CharField(max_length=64,null=True,blank=True)
    description = models.CharField(max_length=127,null=True,blank=True)
    parent= TreeForeignKey("self",on_delete=models.CASCADE,null=True,blank=True,related_name='children')
    is_active = models.BooleanField(default=False)


    class MPTTMeta:
        order_insertion_by = ['name']


    def __str__(self):
        return self.name




class ProductType (models.Model):
    name= models.CharField(max_length=255,unique=True)
    is_active = models.BooleanField(default=True)


    def __str__(self):
        return self.name


class ProductSpecification(models.Model):
    product_type= models.ForeignKey("product.ProductType",on_delete=models.RESTRICT)
    name= models.CharField(max_length=255,)

    def __str__(self):
        return self.name


class ProductSpecificationValue(models.Model):
    product= models.ForeignKey("product.Product", on_delete=models.CASCADE)
    specification= models.ForeignKey("product.ProductSpecification",on_delete=models.RESTRICT)
    value= models.CharField(max_length=255,)

    def __str__(self) :
        return self.value
