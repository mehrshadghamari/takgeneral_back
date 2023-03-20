from django.core.management.base import BaseCommand, CommandError

from product.models import TitleAttribute,ProductCategory,ProductBrand


all_title=['کشور سازنده','حداقل ارتفاع پمپاژ ( کمترین هد )','حداکثر ارتفاع پمپاژ (بیشترین هد)',
           'حداقل میزان آبدهی ( کمترین دبی )','حداکثر میزان آبدهی ( بیشترین دبی )',
           'تعداد پروانه','جنس پروانه','تعداد فاز ','حداکثر تحمل فشار آب ورودی به پمپ',
           'حداکثر دور گردش','طول','عرض','ارتفاع','ولتاژ','وزن','فرکانس','کاربرد محصول'
           ,'نوع سیال یا مواد ','قطر ورودی','قطر خروجی','حداکثر تحمل دمای سیال',
           'جنس بدنه','جنس شافت','جنس آب بند','جنس واسطه','سیل مکانیکی ',
           'جنس سیم پیچ','جنس پوسته و پایه','کاسه سیل','درجه حفاظتی موتور','جریان','کلاس عایق بندی',
           'قابلیت غوطه ور شدن در آب','حداکثر عمق مکش','یاتاقان','خازن','مسیر بای پس','محافظ ( اورلود ) حرارتی']



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



