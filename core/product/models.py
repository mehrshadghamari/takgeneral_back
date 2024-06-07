from django.contrib.contenttypes.fields import GenericRelation
from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Q
from mptt.models import MPTTModel
from mptt.models import TreeForeignKey
from product.managers import CategoryManager
from product.managers import ProductManager
from product.managers import ProductVariantManager


class ProductImage(models.Model):
    image = models.ImageField()
    product = models.ForeignKey(
        "product.Product",
        on_delete=models.CASCADE,
        related_name="images",
    )
    alt_text = models.CharField(
        max_length=255,
        null=True,
    )
    is_main = models.BooleanField(
        default=False,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        null=True,
    )
    upload_at = models.DateTimeField(
        auto_now=True,
        null=True,
    )

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
    name = models.CharField(
        max_length=64,
    )
    logo = models.ImageField(
        null=True,
    )  # new
    url = models.CharField(
        max_length=64,
        null=True,
        unique=True,
        db_index=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        null=True,
    )
    update_at = models.DateTimeField(
        auto_now=True,
        null=True,
    )

    main_banners = GenericRelation(
        "extention.MainBanner",
    )
    banners = GenericRelation(
        "extention.Banner",
    )
    content = GenericRelation(
        "extention.Content",
    )
    meta_tag = GenericRelation(
        "extention.MetaTag",
    )

    def __str__(self):
        return self.name


class ProductAttention(models.Model):
    text = models.CharField(
        max_length=257,
    )
    product = models.ForeignKey(
        "product.Product",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )


class Product(models.Model):
    product_type = models.ForeignKey(
        "product.ProductType",
        null=True,
        blank=True,
        on_delete=models.RESTRICT,
    )
    category = models.ForeignKey(
        "product.Category",
        on_delete=models.RESTRICT,
        null=True,
        db_index=True,
    )
    url = models.SlugField(
        max_length=255,
        unique=True,
        null=True,
        db_index=True,
    )
    name = models.CharField(max_length=64)
    brand = models.ForeignKey(
        "product.ProductBrand",
        on_delete=models.RESTRICT,
        db_index=True,
    )
    special_offer = models.BooleanField(
        default=False,
    )
    pdf = models.FileField(
        null=True,
        blank=True,
    )
    is_active = models.BooleanField(
        default=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        null=True,
    )
    update_at = models.DateTimeField(
        auto_now=True,
        null=True,
    )

    content = GenericRelation(
        "extention.Content",
    )
    meta_tag = GenericRelation(
        "extention.MetaTag",
    )

    objects = ProductManager()

    @property
    def attributes(self):
        return self.productspecificationvalue_set.all()

    @property
    def main_image(self):
        return self.images.filter(is_main=True).first()

    @property
    def all_images(self):
        return self.images.all()

    @property
    def options(self):
        return self.options.all()

    @property
    def attentions(self):
        return self.productattention_set.all()

    @property
    def prices(self):
        product_variants = ProductVariant.objects.filter(option__product_id=self.id)
        prices = [
            {
                "price": variant.price,
                "final_price": variant.final_price,
                "discount": variant.discount,
            }
            for variant in product_variants
        ]
        return prices

    @property
    def min_price(self):
        product_variants = ProductVariant.objects.filter(option__product_id=self.id)

        if not product_variants:
            return None  # No variants, so return None or appropriate default

        # Find the variant with the minimum price
        min_variant = min(product_variants, key=lambda variant: variant.final_price)

        # Create a dictionary containing the minimum price information
        min_price_info = {
            "price": min_variant.price,
            "final_price": min_variant.final_price,
            "discount": min_variant.discount,
        }

        return min_price_info

    @property
    def lowest_price(self):
        variants = ProductVariant.objects.filter(option__product=self)
        if variants.exists():
            return min(variant.final_price for variant in variants)
        return 0  # Default value if no variants exist

    @property
    def similar_product_ids(self):
        max_price = self.lowest_price + 1000000
        min_price = self.lowest_price - 1000000

        similar_product_ids = (
            ProductVariant.objects.select_related("option__product")
            .filter(
                ~Q(option__product__id=self.id),
                price__lte=max_price,
                price__gte=min_price,
            )
            .values_list("option__product__id", flat=True)
        )

        unique_similar_product_ids = list(set(similar_product_ids))

        return unique_similar_product_ids

    def get_variant_with_min_final_price(self, variants):
        min_final_price = float("inf")
        selected_variant = None

        for variant in variants:
            if variant.final_price is not None and variant.final_price < min_final_price:
                min_final_price = variant.final_price
                selected_variant = variant

        return selected_variant

    def get_variant_with_max_discount(self, variants):
        max_discount = float("-inf")
        selected_variant = None

        for variant in variants:
            if variant.discount is not None and variant.discount > max_discount:
                max_discount = variant.discount
                selected_variant = variant

        return selected_variant

    @property
    def best_price(self):
        product_variants = ProductVariant.objects.filter(option__product_id=self.id)

        if not product_variants:
            return None  # No variants, so return None or appropriate default

        variant_with_min_final_price = self.get_variant_with_min_final_price(product_variants)
        variant_with_max_discount = self.get_variant_with_max_discount(product_variants)

        if variant_with_min_final_price is None or variant_with_max_discount is None:
            return None  # No valid variants found

        if variant_with_min_final_price == variant_with_max_discount:
            # If the same variant has both min final price and max discount, return it
            return {
                "price": variant_with_min_final_price.price,
                "final_price": variant_with_min_final_price.final_price,
                "discount": variant_with_min_final_price.discount,
            }

        return {
            "price": variant_with_min_final_price.price,
            "final_price": variant_with_min_final_price.final_price,
            "discount": variant_with_max_discount.discount,
        }

    def __str__(self):
        return f"id : {self.id} -- name : {self.name} "


class ProductOptionType(models.Model):
    product = models.OneToOneField(
        Product,
        on_delete=models.CASCADE,
        null=True,
        related_name="options",
    )
    name = models.CharField(
        max_length=127,
        null=True,
        blank=True,
    )
    no_option = models.BooleanField(
        default=False,
    )

    @property
    def product_variant(self):
        return self.values.all()


class ProductVariant(models.Model):
    made_in_chiose = (
        ("کالای اورجینال", "کالای اورجینال"),
        ("کالای ایرانی", "کالای ایرانی"),
    )

    option = models.ForeignKey(
        ProductOptionType,
        on_delete=models.CASCADE,
        related_name="values",
    )
    option_value = models.CharField(
        max_length=127,
        null=True,
        blank=True,
    )
    price = models.FloatField()
    discount = models.PositiveSmallIntegerField(
        default=0,
        validators=[MaxValueValidator(99), MinValueValidator(0)],
    )
    Inventory_number = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0)],
    )
    made_in = models.CharField(
        max_length=25,
        choices=made_in_chiose,
        null=True,
        blank=True,
    )
    min_price = models.BooleanField()
    free_send = models.BooleanField()
    waranty_tamir = models.BooleanField()
    waranty_taviz = models.BooleanField()
    month_of_waranty = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
    )
    created_at = models.DateField(
        auto_now_add=True,
        null=True,
    )
    update_at = models.DateField(
        auto_now=True,
        null=True,
    )

    objects = ProductVariantManager()

    @property
    def final_price(self):
        if self.discount == 0:
            final_price = self.price
        else:
            final_price = float(self.price - (self.price * self.discount / 100))
        return final_price

    @property
    def product_id(self):
        return self.option.product.id

    @property
    def product_url(self):
        return self.option.product.url

    @property
    def product_name(self):
        return self.option.product.name

    @property
    def product_main_image(self):
        return self.option.product.main_image

    @property
    def product_available(self):
        if self.Inventory_number > 0:
            available = True
        else:
            available = False

        return available

    @property
    def warranty(self):
        if self.waranty_tamir == False and self.waranty_taviz == False:
            warranty = ""

        elif self.waranty_taviz == False:
            warranty = f"{self.month_of_waranty} ماه گارانتی تعمیر "

        elif self.waranty_tamir == False:
            warranty = f"{self.month_of_waranty} ماه گارانتی تعویض "

        elif self.waranty_taviz == True and self.waranty_tamir == True:
            warranty = f" {self.month_of_waranty} ماه گارانتی تعویض و تعمیر "

        return warranty

    @property
    def inventory_status(self):
        status = ""

        if self.Inventory_number == 0 or None:
            status = "کالا موجود نیست"
        if self.Inventory_number > 0 and self.Inventory_number <= 3:
            status = f"عدد ازاین کالا موجود هست {self.Inventory_number}"
        if self.Inventory_number >= 4:
            status = "کالا موحود هست"

        return status


# for release 2


class Category(MPTTModel):
    name = models.CharField(
        max_length=255,
        unique=True,
    )
    url = models.SlugField(
        max_length=255,
        unique=True,
        db_index=True,
    )
    image = models.ImageField(
        null=True,
        blank=True,
    )
    alt_text = models.CharField(
        max_length=64,
        null=True,
        blank=True,
    )
    description = models.CharField(
        max_length=127,
        null=True,
        blank=True,
    )
    parent = TreeForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
    )
    is_active = models.BooleanField(
        default=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        null=True,
    )
    update_at = models.DateTimeField(
        auto_now=True,
        null=True,
    )

    main_banners = GenericRelation(
        "extention.MainBanner",
    )
    banners = GenericRelation(
        "extention.Banner",
    )
    content = GenericRelation(
        "extention.Content",
    )
    meta_tag = GenericRelation(
        "extention.MetaTag",
    )

    objects = CategoryManager()

    class MPTTMeta:
        order_insertion_by = [
            "name",
        ]

    def __str__(self):
        return self.name


class ProductType(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(
        default=True,
    )

    def __str__(self):
        return self.name


class ProductSpecification(models.Model):
    product_type = models.ForeignKey(
        ProductType,
        on_delete=models.RESTRICT,
    )
    name = models.CharField(
        max_length=255,
    )

    def __str__(self):
        return self.name


class ProductSpecificationValue(models.Model):
    product = models.ForeignKey(
        "product.Product",
        on_delete=models.CASCADE,
    )
    specification = models.ForeignKey(
        "product.ProductSpecification",
        on_delete=models.RESTRICT,
    )
    value = models.CharField(
        max_length=255,
    )
    search_value = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.value

    class Meta:
        ordering = [
            "specification",
        ]


# class FilterOptionType(models.Model):
#     name = models.CharField(max_length=50, unique=True)
#     options = models.CharField(max_length=500, blank=True)  # Store options as a comma-separated string for enum

#     @property
#     def get_options(self):
#         if self.options:
#             return self.options.split(',')
#         return []

#     def __str__(self):
#         return self.name


# class FilterOption(models.Model):
#     category = models.ForeignKey("product.Category", on_delete=models.CASCADE, related_name='filter_options')
#     specification_name = models.CharField(max_length=255,null=True)
#     filter_option_type = models.OneToOneField("product.FilterOptionType", on_delete=models.SET_NULL, null=True, blank=True)
#     min_value = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
#     max_value = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

#     def __str__(self):
#         return self.specification_name if self.specification_name else ""
