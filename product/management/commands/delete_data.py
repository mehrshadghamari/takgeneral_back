from django.core.management.base import BaseCommand

from product.models import Category
from product.models import Product
from product.models import ProductBrand

all_model = [Product, ProductBrand, Product, Category]


class Command(BaseCommand):
    help = 'create some data'

    def handle(self, *args, **options):
        for M in all_model:
            instances = M.objects.all()
            instances.delete()
