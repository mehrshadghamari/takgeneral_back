from django.db import models
from django.db.models import F,Q
from django.core.validators import MaxValueValidator, MinValueValidator
from .choices import keshvar_sazande_choice,kase_seyl_choice,khazen_choice,faz_choice,volt_choice,jense_ababand_choice,jense_badane_choice,jense_parvane_choice,jense_shaft_choice,jense_simpich_choice,jense_vaset_choice,jese_poste_va_paye_choice,daraje_hefazati_motor_choice,yataghan_choice

# Create your models here.


class ProductImage(models.Model):
    image=models.ImageField()
    product=models.ForeignKey('product.Product',on_delete=models.CASCADE,related_name='other_images')




# category many to many
class ProductCategory(models.Model):
    name=models.CharField(max_length=255)

    def __str__(self):
        return self.name
    


class ProductBrand(models.Model):
    name=models.CharField(max_length=64)
    image=models.ImageField(null=True)

    def __str__(self) :
        return self.name


class ProductManager(models.manager):
    def with_final_price(self):
        self.annotate(final_price=F('price')-(F('price')*F('discount')/100))



class Product(models.Model):
    objects= ProductManager() 

    name=models.CharField(max_length=64)
    # country=models.CharField(max_length=64,choices=keshvar_sazande_choice)
    category=models.ManyToManyField('product.ProductCategory')
    brand=models.ForeignKey('product.ProductBrand',on_delete=models.CASCADE)
    model_brand=models.CharField(max_length=64)
    main_image=models.ImageField()
    count_of_product=models.IntegerField(default=1)
    discount=models.IntegerField(default=0,validators=[MaxValueValidator(99), MinValueValidator(0)])
    price=models.FloatField()
    special_offer=models.BooleanField(default=False)
    seven_days_back=models.BooleanField(default=False)
    free_send=models.BooleanField(default=True)
    waranty_tamir=models.BooleanField()
    waranty_taviz=models.BooleanField()
    month_of_waranty=models.IntegerField()


    @property
    def other_images(self):
        return self.other_images.all()


    @property
    def final_price(self):
        if self.discount==0:
            return self.price
        return self.price - self.price*(self.discount/100)


    @property
    def product_available(self):
        if self.count_of_product==0:
            return False
        return True

    @property
    def warranty(self):
        if self.waranty_tamir==False and self.waranty_taviz==False:
            return ''

        elif self.waranty_taviz==False:
            return f'{self.month_of_waranty} ماه گارانتی تعمیر '

        elif self.waranty_tamir==False:
            return f'{self.month_of_waranty} ماه گارانتی تعویض '

        elif self.waranty_taviz==True and self.waranty_tamir==True:
            return f' {self.month_of_waranty} ماه گارانتی تعویض و تعمیر '



    def __str__(self):
        return  f'id : {self.id} -- name : {self.name} ' 


class TitleAttribute(models.Model):
    name=models.CharField(max_length=127)

    def __str__(self):
        return self .name



class Attribute(models.Model):
    title=models.ForeignKey('product.TitleAttribute',on_delete=models.CASCADE)
    value=models.CharField(max_length=127)
    product=models.ForeignKey('product.Product',on_delete=models.CASCADE,related_name='attributes')

    def __str__(self):
        return f'{self.title}  -  {self.value} -  for {self.product.name}'

    # power=models.FloatField(verbose_name='tavane')
    # min_head=models.FloatField(verbose_name='hadeaghal ertefae popmaj')
    # max_head=models.FloatField(verbose_name='hadeaksare ertefae popmaj')
    # min_deby=models.FloatField(verbose_name='hadeaghal mizane ab dehi')
    # max_deby=models.FloatField(verbose_name='hadeaksare mizane ab dehi')
    # armicher_kind=models.CharField(verbose_name='jense parvane',max_length=64,choices=jense_parvane_choice)
    # count_of_armicher=models.IntegerField(verbose_name="tedade parvene")
    # count_of_phase=models.CharField(verbose_name='tedade faz',max_length=64,choices=faz_choice)
    # max_pressure_pomp=models.FloatField(verbose_name='hade akaser tahamol abe vorodi be popm')
    # max_rpm=models.IntegerField(verbose_name='hade aksar dore gardesh')
    # l=models.FloatField()
    # w=models.FloatField()
    # h=models.FloatField()
    # voltage=models.CharField(verbose_name='voltaj',max_length=64,choices=volt_choice)
    # weight=models.IntegerField(verbose_name='vaszn')
    # frequency=models.IntegerField(verbose_name='ferekanse')
    # usage=models.CharField(verbose_name='karborde mahsol ',max_length=64)
    # input_diameter=models.FloatField(verbose_name='ghotre vorodi')
    # out_diameter=models.FloatField(verbose_name='ghotre khoroji')
    # fluid_type=models.CharField(verbose_name='noe sayal ya mavad',max_length=64)
    # max_temperature=models.CharField(verbose_name='hade aksar damaye tahaamol sayal',max_length=64)
    # body_kind=models.CharField(verbose_name='jense badane',max_length=64,choices=jense_badane_choice)
    # shaft_kind=models.CharField(verbose_name='jense shaft',max_length=64,choices=jense_shaft_choice)
    # water_block=models.CharField(verbose_name='jense abband',max_length=64,choices=jense_ababand_choice)
    # between_kind=models.CharField(verbose_name='jense vasete',max_length=64,choices=jense_vaset_choice)
    # mechanic_sail=models.CharField(verbose_name='saile mekanici',max_length=64)
    # protectical_dgree_od_motor=models.CharField(verbose_name='daraje hefazati motor',max_length=64,choices=daraje_hefazati_motor_choice)
    # flow=models.FloatField(verbose_name='jaryan')
    # insulation_class=models.CharField(verbose_name='kelase ayegh bandi',max_length=64)
    # to_dive_in_water=models.BooleanField(verbose_name='ghabeliyat ghote var shodan dar ab',default=None)
    # bearinge=models.CharField(verbose_name='yataghan',max_length=64,choices=yataghan_choice)
    # khazen=models.CharField(verbose_name='khazen',max_length=64,choices=khazen_choice)



    # @property
    # def waranty(self):
        # if self.waranty_tamir==False and self.waranty_taviz==False:
            # return f'گارانتی تعویض و تعمیر ندارد'
        # 
        # elif self.waranty_taviz==False:
            # return f'{self.month_of_waranty}  ماه گارانتی   {self.waranty_tamir} '
        # 
        # elif self.waranty_tamir==False:
            # return f'{self.month_of_waranty}  ماه گارانتی   {self.waranty_taviz} '
        # 
        # elif self.waranty_taviz==True and self.waranty_tamir==True:
            # return f'{self.month_of_waranty}  ماه گارانتی   {self.waranty_taviz} و {self.waranty_tamir} '


    # @property
    # def horse_power(self):
        # self.power*1.34



    # class Meta:
        # abstract = True
# 


# class HomePomp(BasePomp):
    # home_type_choice=(
    # ('جتی','jeti'),(''),(),()
    # )
    # home_type=models.CharField(max_length=10)
    # silver_kind=models.CharField(verbose_name='jense simpisch',max_length=64,choices=jense_simpich_choice)
    # jense_poste_ya_paye=models.CharField(max_length=64,choices=jese_poste_va_paye_choice)
    # kase_sail=models.CharField(max_length=64,choices=kase_seyl_choice)
    # hadeaksar_omghe_makesh=models.CharField(max_length=64)
    # masire_bay_pas=models.BooleanField(null=True)
    # mohafeze_hararti=models.BooleanField(null=True)



    # @property
    # def title(self):
        # f'{self.type} + {self.home_type} + {self.horse_power} + {self.model_brand} + {self.brand} '


    # @property
    # def similar_pomp(self):
        # return HomePomp.objects.filter(voltage__gte=self.voltage-.5,voltage__lte=self.voltage+.5)



