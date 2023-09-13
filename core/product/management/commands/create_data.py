import random
import uuid

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.text import slugify
from product.models import Category
from product.models import Product
from product.models import ProductBrand
from product.models import ProductOptionType
from product.models import ProductVariant

all_brand = ['پمپ پنتاکس pentax', 'ابارا Ebara', 'پمپ دیزل ساز Dieselsaz', 'پمپ ورتکس wortex', 'پمپ لئو Leo',
             'پمپ الکتروژن Electrogen', 'پمپ گراندفوس Grundfos']

main_categories = [
    'پمپ',
    'ابزار دقیق',
    'کولر',
    'فلومتر',
]

subcategories = [
    ('پمپ اب خانگی', 0),
    # The second element in each tuple represents the index of the main category it belongs to (0-based).
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
    ('پمپ آب بشقابی', 0),
    # The second element in each tuple represents the index of the subcategory it belongs to (0-based).
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
                main_category = Category.objects.create(name=main_category_name, url=main_category_slug,
                                                        is_active=True)

                # Create subcategories
                for subcategory_name, main_category_index in subcategories:
                    if main_category_index == main_categories.index(main_category_name):
                        subcategory_slug = slugify(str(uuid.uuid4()))
                        subcategory = Category.objects.create(name=subcategory_name, url=subcategory_slug,
                                                              parent=main_category, is_active=True)

                        # Create sub-subcategories
                        for sub_subcategory_name, subcategory_index in sub_subcategories:
                            if subcategory_index == subcategories.index((subcategory_name, main_category_index)):
                                sub_subcategory_slug = slugify(str(uuid.uuid4()))
                                Category.objects.create(name=sub_subcategory_name, url=sub_subcategory_slug,
                                                        parent=subcategory, is_active=True)

            # create brands
            for b in all_brand:
                ProductBrand.objects.create(name=b)

            # create products
            for i in range(1500):
                brand_instance = ProductBrand.objects.order_by('?')[0]
                category_instance = Category.objects.filter(children__isnull=True).order_by('?')[0]

                name = f"محصول - {i + 1} <{category_instance.name}> "
                url = slugify(name + category_instance.name + brand_instance.name)

                # Create the product object
                product_instance = Product.objects.create(
                    name=name,
                    url=url,
                    brand=brand_instance,
                    category=category_instance,
                    special_offer=random.choice([True, False])
                )
                no_option = random.choice([True, False])
                if not no_option:
                    option_instance = ProductOptionType.objects.create(product=product_instance,
                                                                       name=random.choice(['مایع', 'گاز']))
                    for i in range(1, 4):
                        Inventory_number = random.randint(1, 100)
                        discount = random.randint(0, 50)
                        price = round(random.randint(1000000, 10000000))
                        min_price = random.choice([True, False])
                        free_send = random.choice([True, False])
                        waranty_tamir = random.choice([True, False])
                        waranty_taviz = random.choice([True, False])
                        month_of_waranty = random.choice([6, 12, 24])

                        ProductVariant.objects.create(
                            option=option_instance,
                            option_value=f' لیتر{i}000',
                            Inventory_number=Inventory_number,
                            discount=discount,
                            price=price,
                            min_price=min_price,
                            free_send=free_send,
                            waranty_tamir=waranty_tamir,
                            waranty_taviz=waranty_taviz,
                            month_of_waranty=month_of_waranty,
                        )
                else:
                    option_instance = ProductOptionType.objects.create(product=product_instance, no_option=True)
                    Inventory_number = random.randint(1, 100)
                    discount = random.randint(0, 50)
                    price = round(random.randint(1000000, 10000000))
                    min_price = random.choice([True, False])
                    free_send = random.choice([True, False])
                    waranty_tamir = random.choice([True, False])
                    waranty_taviz = random.choice([True, False])
                    month_of_waranty = random.choice([6, 12, 24])
                    made_in = random.choice(['کالای ایرانی', 'کالای اورجینال'])

                    ProductVariant.objects.create(
                        option=option_instance,
                        option_value=None,
                        Inventory_number=Inventory_number,
                        discount=discount,
                        price=price,
                        made_in=made_in,
                        min_price=min_price,
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
