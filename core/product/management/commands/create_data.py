from django.core.management.base import BaseCommand, CommandError

from product.models import TitleAttribute,ProductCategory,ProductBrand


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



