from django.db import models
from django.db.models import F
from django.db.models import Min
from django.db.models import OuterRef
from django.db.models import Subquery


class ProductVariantManager(models.Manager):
    def with_final_price(self):
        return self.get_queryset().annotate(final_price_manager=F('price') - (F('price') * F('discount') / 100))


class ProductManager(models.Manager):
    def with_lowest_price(self):
        from .models import ProductVariant
        lowest_prices_subquery = (
            ProductVariant.objects.with_final_price().filter(option__product=OuterRef('pk'))
            .values('option__product')
            .annotate(lowest_price=Min('final_price_manager'))
            .values('lowest_price')
        )

        return self.get_queryset().annotate(
            lowest_price=Subquery(lowest_prices_subquery, output_field=models.FloatField())
        )
