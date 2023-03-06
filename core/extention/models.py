from django.db import models

# Create your models here.

class Slider(models.Model):
    # type_choise=(
        # ('mobile','mobile'),
        # ('pc','pc'),
    # )
    name=models.CharField(max_length=40)
    mobile_image=models.ImageField()
    pc_image=models.ImageField()
    # type=models.CharField(choices=type_choise,max_length=10) 