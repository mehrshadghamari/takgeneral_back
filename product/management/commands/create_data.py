import base64
import random
import uuid
from datetime import datetime
from datetime import timedelta

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.text import slugify
from django.utils.timezone import make_aware
from product.models import Category
from product.models import Product
from product.models import ProductBrand
from product.models import ProductImage

all_brand=['پمپ پنتاکس pentax','ابارا Ebara','پمپ دیزل ساز Dieselsaz','پمپ ورتکس wortex','پمپ لئو Leo','پمپ الکتروژن Electrogen','پمپ گراندفوس Grundfos']



main_categories = [
    'پمپ',
    'ابزار دقیق',
    'کولر',
    'فلومتر',
]

subcategories = [
    ('پمپ اب خانگی', 0),  # The second element in each tuple represents the index of the main category it belongs to (0-based).
    ('پمپ آب طبقاتی', 0),
    ('پمپ آب کشاورزی و صنعتی', 0),
    ('پمپ سیرکولاتور یا پمپ شوفاژ', 0),
    ('پمپ استخری', 0),
    ('پمپ شناور یا پمپ چاه', 0),
    ('لوازم جانبی پمپ', 0),
    ('تجهیزات کنترل', 1),
    ('کولر گازی یا اسپیلت پرتابل', 2),
    ('کولر گازی یا اسپیلت دیواری', 2),
    ('برند های کولر گازی یا اسپیلت', 2),
]


sub_subcategories = [
    ('پمپ آب بشقابی', 0),  # The second element in each tuple represents the index of the subcategory it belongs to (0-based).
    ('پمپ آب جتی', 0),
    ('پمپ آب دو پروانه', 0),
    ('پمپ آب محیطی', 0),
    ('شیر برقی گاز', 7),
    ('کولر گازی ایران رادیاتور', 10),
]



class Command(BaseCommand):
    help = 'create some data'


    def handle(self, *args, **options):
        with transaction.atomic():
         # Create main categories

            for main_category_name in main_categories:

                main_category_slug = slugify(str(uuid.uuid4()))
                main_category = Category.objects.create(name=main_category_name, slug=main_category_slug, is_active=True)

                # Create subcategories
                for subcategory_name, main_category_index in subcategories:
                    if main_category_index == main_categories.index(main_category_name):
                        subcategory_slug = slugify(str(uuid.uuid4()))
                        subcategory = Category.objects.create(name=subcategory_name, slug=subcategory_slug, parent=main_category, is_active=True)

                        # Create sub-subcategories
                        for sub_subcategory_name, subcategory_index in sub_subcategories:
                            if subcategory_index == subcategories.index((subcategory_name, main_category_index)):
                                sub_subcategory_slug = slugify(str(uuid.uuid4()))
                                Category.objects.create(name=sub_subcategory_name, slug=sub_subcategory_slug, parent=subcategory, is_active=True)


        # create brands
            for b in all_brand:
                ProductBrand.objects.create(name=b)



        # create products
            for i in range(1500):

                brand_instance = ProductBrand.objects.order_by('?')[0]
                category_instance =  Category.objects.filter(children__isnull=True).order_by('?')[0]

                name = f"محصول - {i+1} <{category_instance.name}> "
                slug =slugify(name + category_instance.name + brand_instance.name)
                count_of_product = random.randint(1, 100)
                discount = random.randint(0, 50)
                price = round(random.randint(1000000, 10000000))
                special_offer = random.choice([True, False])
                seven_days_back = random.choice([True, False])
                free_send = random.choice([True, False])
                waranty_tamir = random.choice([True, False])
                waranty_taviz = random.choice([True, False])
                month_of_waranty = random.choice([6, 12, 24])


                # Create the product object
                product_instance = Product.objects.create(
                    name=name,
                    slug= slug,
                    brand= brand_instance,
                    category = category_instance,
                    count_of_product=count_of_product,
                    discount=discount,
                    price=price,
                    special_offer=special_offer,
                    seven_days_back=seven_days_back,
                    free_send=free_send,
                    waranty_tamir=waranty_tamir,
                    waranty_taviz=waranty_taviz,
                    month_of_waranty=month_of_waranty,
                )



                ######### image for product ##########

                # for i, base64_image in enumerate(images):
                #     is_main = False
                #     if i ==0:
                #         is_main=True

                #     if ";base64," not in base64_image:
                #         # Skip the image if the delimiter is not present
                #         continue

                #     img_parts = base64_image.split(";base64,")
                #     if len(img_parts) != 2:
                #         # Skip the image if it doesn't contain the expected two parts
                #         continue

                #     img_format, imgstr = img_parts
                #     ext = img_format.split("/")[-1]
                #     image_data = ContentFile(base64.b64decode(imgstr), name=f'{str(uuid.uuid4())}.' + ext)

                #     ProductImage.objects.create(image= image_data,is_main=is_main,alt_text="testing alt text" )


            self.stdout.write(self.style.SUCCESS("Successfully create data"))
