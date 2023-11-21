from django.db import models
from django.db.models import F
from django.db.models import Max
from django.db.models import Min
from django.db.models import OuterRef
from django.db.models import Subquery


class ProductVariantManager(models.Manager):
    def with_final_price(self):
        return self.get_queryset().annotate(final_price_manager=F("price") - (F("price") * F("discount") / 100))


class ProductManager(models.Manager):
    def with_price_info(self):
        from .models import ProductVariant

        prices_subquery = (
            ProductVariant.objects.with_final_price()
            .select_related("option__product")
            .filter(option__product=OuterRef("pk"))
            .values("option__product")
            .annotate(lowest_price=Min("price"), lowest_final_price=Min("final_price_manager"), highest_discount=Max("discount"))
            # .values('lowest_price')
        )

        return self.get_queryset().annotate(
            lowest_price_manager=Subquery(prices_subquery.values("lowest_price"), output_field=models.FloatField()),
            lowest_final_price_manager=Subquery(prices_subquery.values("lowest_final_price"), output_field=models.FloatField()),
            highest_discount_manager=Subquery(prices_subquery.values("highest_discount"), output_field=models.IntegerField()),
        )
