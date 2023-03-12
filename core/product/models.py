from django.db import models

# Create your models here.

class BasePomp (models.Model):
    type=models.CharField(verbose_name='daste bandi pomp')
    brand=models.ForeignKey('extention.brand',on_delete=models.SET_NULL)
    model_brand=models.CharField()
    name=models.CharField(verbose_name='name pomp')
    country=models.CharField(verbose_name='keshavare sazande')
    warranty=models.CharField(verbose_name='granti')
    power=models.FloatField(verbose_name='tavane')
    min_head=models.FloatField(verbose_name='hadeaghal ertefae popmaj')
    max_head=models.FloatField(verbose_name='hadeaksare ertefae popmaj')
    min_deby=models.FloatField(verbose_name='hadeaghal mizane ab dehi')
    max_deby=models.FloatField(verbose_name='hadeaksare mizane ab dehi')
    armicher_kind=models.CharField(verbose_name='gense parvane')
    count_of_armicher=models.IntegerField(verbose_name="tedade parvene")
    count_of_phase=models.IntegerField(verbose_name='tedade faz')
    max_pressure_pomp=models.FloatField(verbose_name='hade akaser tahamol abe vorodi be popm')
    max_rpm=models.IntegerField(verbose_name='hade aksar dore gardesh')
    l=models.FloatField()
    w=models.FloatField()
    h=models.FloatField()
    voltage=models.IntegerField(verbose_name='voltaj')
    weight=models.IntegerField(verbose_name='vaszn')
    frequency=models.IntegerField(verbose_name='ferekanse')
    usage=models.CharField(verbose_name='karborde mahsol ')
    input_diameter=models.FloatField(verbose_name='ghotre vorodi')
    out_diameter=models.FloatField(verbose_name='ghotre khoroji')
    fluid_type=models.CharField(verbose_name='noe sayal ya mavad')
    max_tamperature=models.ImageField(verbose_name='hade aksar damaye tahaamol sayal')
    body_kind=models.CharField(verbose_name='gense badane')
    shaft_kind=models.CharField(verbose_name='gense shaft')
    water_block=models.CharField(verbose_name='gense abband')
    between_kind=models.CharField(verbose_name='gense vasete')
    mechanic_sail=models.CharField(verbose_name='saile mekanici')
    protectical_dgree_od_motor=models.CharField(verbose_name='daraje hefazati motor')
    flow=models.FloatField(verbose_name='jaryan')
    insulation_class=models.CharField(verbose_name='kelase ayegh bandi')
    to_dive_in_water=models.CharField(verbose_name='ghabeliyat ghote var shodan dar ab')
    bearinge=models.CharField(verbose_name='yataghan')
    khazen=models.CharField(verbose_name='khazen')



class HomePomp(BasePomp):
    home_type_choice=(
    ('جتی'),(''),(),()
    )
    home_type=models.CharField(choices=home_type_choice,max_length=10)
    silver_kind=models.CharField(verbose_name='gense simpisch')
    gense_poste_ya_paye=models.CharField()
    kase_sail=models.CharField()
    hadeaksar_omghe_makesh=models.CharField()
    masire_bay_pas=models.NullBooleanField()
    mohafeze_hararti=models.NullBooleanField()




    def name(self):
        self.type + self.home_type + self.model_brand+self.brand





