import random
from datetime import timedelta, datetime
from django.core.management.base import BaseCommand
from django.utils.timezone import make_aware
from product.models import TitleAttribute,ProductCategory,ProductBrand,Product



all_title=['کشور سازنده','توان','حداقل ارتفاع پمپاژ ( کمترین هد )','حداکثر ارتفاع پمپاژ (بیشترین هد)',
           'حداقل میزان آبدهی ( کمترین دبی )','حداکثر میزان آبدهی ( بیشترین دبی )',
           'تعداد پروانه','جنس پروانه','تعداد فاز ','حداکثر تحمل فشار آب ورودی به پمپ',
           'حداکثر دور گردش','طول','عرض','ارتفاع','ولتاژ','وزن','فرکانس','کاربرد محصول'
           ,'نوع سیال یا مواد','قطر ورودی','قطر خروجی','حداکثر تحمل دمای سیال',
           'جنس بدنه','جنس شافت','جنس آب بند','جنس واسطه','سیل مکانیکی ',
           'جنس سیم پیچ','جنس پوسته و پایه','کاسه سیل','درجه حفاظتی موتور','جریان','کلاس عایق بندی',
           'قابلیت غوطه ور شدن در آب','حداکثر عمق مکش','یاتاقان','خازن','مسیر بای پس','محافظ ( اورلود ) حرارتی']


product_json={
        'values':{
                'country': {
                    'name':'کشور سازنده',
                    'value':''
                },
                'tavan':{
                    'name':'توان',
                    'value':'',
                },
                'min_head':{
                    'name':'حداقل ارتفاع پمپاژ ( کمترین هد )',
                    'value':''
                },
                'max_head':{
                    'name':'حداکثر ارتفاع پمپاژ (بیشترین هد)',
                    'value':''                    
                },
                'min_deby':{
                    'name':'حداقل میزان آبدهی ( کمترین دبی )',
                    'value':''
                },
                'max_deby':{
                    'name':'حداکثر میزان آبدهی ( بیشترین دبی )',
                    'value':''
                },
                'tedad_parvane':{
                    'name':'تعداد پروانه',
                    'value':''
                },
                'tedad_faz':{
                    'name':'تعداد فاز',
                    'value':''
                },
                'hade_aksar_feshar_ab':{
                    'name':'حداکثر تحمل فشار آب ورودی به پمپ',
                    'value':''
                },
                'hade_aksar_doregardesh':{
                    'name':'حداکثر دور گردش',
                    'value':''
                },
                'voltaj':{
                    'name':'ولتاژ',
                    'value':''
                },
                'vazn':{
                    'name':'وزن',
                    'value':''
                },
                'ferekans':{
                    'name':'فرکانس',
                    'value':''
                },
                'karbord_mahsol':{
                    'name':'کاربرد محصول',
                    'value':''
                },
                'noe_sayal':{
                    'name':'نوع سیال یا مواد',
                    'value':''
                },
                'ghotre_vorodi':{
                    'name':'قطر ورودی',
                    'value':''
                },
                'ghotre_khoroji':{
                    'name':'قطر خروجی',
                    'value':''
                },
                'hadeaksar_dama_sayal':{
                    'name':'حداکثر تحمل دمای سیال',
                    'value':''
                },
                'jense_parvane':{
                    'name':'جنس پروانه',
                    'value':''
                },
                'jense_parvane':{
                    'name':'جنس پروانه',
                    'value':''
                }
            },

            'search_value':{
                    'tavan':{
                        'name':'توان',
                        'value':''
                        },
                    'min_head':{
                        'name':'حداقل ارتفاع پمپاژ ( کمترین هد )',
                        'value':''
                        },
                    'max_head':{
                        'name':'حداکثر ارتفاع پمپاژ (بیشترین هد)',
                        'value':''                    
                        },
                    'min_deby':{
                        'name':'حداقل میزان آبدهی ( کمترین دبی )',
                        'value':''
                        },
                    'max_deby':{
                        'name':'حداکثر میزان آبدهی ( بیشترین دبی )',
                        'value':''
                        }

                }
                
                
              }



all_category=['پمپ','پمپ اب خانگی','پمپ اب خانگی محیطی','پمپ اب خانگی بشقابی','پمپ اب خانگی جتی','پمپ اب خانگی دو پروانه',]


all_brand=['پمپ پنتاکس pentax','ابارا Ebara','پمپ دیزل ساز Dieselsaz','پمپ ورتکس wortex','پمپ لئو Leo','پمپ الکتروژن Electrogen','پمپ گراندفوس Grundfos']



class Command(BaseCommand):
    help = 'create some data'


    def handle(self, *args, **options):
        for c in all_category:
            ProductCategory.objects.create(name=c)

        for a in all_title:
            TitleAttribute.objects.create(name=a)

        for b in all_brand:
            ProductBrand.objects.create(name=b)


        mohiti_category=ProductCategory.objects.filter(name__in=['پمپ','پمپ اب خانگی','پمپ اب خانگی محیطی'])
        boshghabi_category=ProductCategory.objects.filter(name__in=['پمپ','پمپ اب خانگی','پمپ اب خانگی بشقابی'])
        jeti_category=ProductCategory.objects.filter(name__in=['پمپ','پمپ اب خانگی','پمپ اب خانگی جتی'])
        doparvane_category=ProductCategory.objects.filter(name__in=['پمپ','پمپ اب خانگی','پمپ اب خانگی دو پروانه'])

        # Generate random data for the mohiti
        for i in range(60):
            name = f"Pomp khanegi mohiti {i+1}"
            model_brand = f"Model p-m {i+1}"
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
            product = Product.objects.create(
                name=name,
                brand=ProductBrand.objects.order_by('?')[0],
                model_brand=model_brand,
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
            product.category.set(mohiti_category)
            # Generate random data for the boshghabi
        for i in range(60):
            name = f"Pomp khanegi boshghabi {i+1}"
            model_brand = f"Model p-b {i+1}"
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
            product = Product.objects.create(
                name=name,
                brand=ProductBrand.objects.order_by('?')[0],
                model_brand=model_brand,
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
            product.category.set(boshghabi_category)
            # Generate random data for the jeti
        for i in range(60):
            name = f"Pomp khanegi jeti {i+1}"
            model_brand = f"Model p-j {i+1}"
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
            product = Product.objects.create(
                name=name,
                brand=ProductBrand.objects.order_by('?')[0],
                model_brand=model_brand,
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
            product.category.set(jeti_category)

                # Generate random data for the doparvane
        for i in range(60):
            name = f"Pomp khanegi doparvane {i+1}"
            model_brand = f"Model p-dp {i+1}"
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
            product = Product.objects.create(
                name=name,
                brand=ProductBrand.objects.order_by('?')[0],
                model_brand=model_brand,
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
            product.category.set(doparvane_category)

