import random
from datetime import timedelta, datetime
from django.core.management.base import BaseCommand
from django.utils.timezone import make_aware
from product.models import TitleAttribute,ProductCategory,ProductBrand,Product


all_model=[TitleAttribute,ProductCategory,ProductBrand,Product]

class Command(BaseCommand):
    help = 'create some data'


    def handle(self, *args, **options):
        for M in all_model:
            instances=M.objects.all()
            instances.delete()
