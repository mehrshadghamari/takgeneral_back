import random
from datetime import datetime
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils.timezone import make_aware
from product.models import Product
from product.models import ProductBrand
from product.models import ProductCategory
from product.models import TitleAttribute

all_model=[TitleAttribute,ProductCategory,ProductBrand,Product]

class Command(BaseCommand):
    help = 'create some data'


    def handle(self, *args, **options):
        for M in all_model:
            instances=M.objects.all()
            instances.delete()
