import os
from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from product.models import Product
from product.choices import pomp_json


@receiver(post_save,sender=Product)
def create_JsonField(sender, instance, created, **kwargs):
    if created:
        if 'پمپ اب خانگی' in [i.name for i in  instance.category.all()]:
            Product.objects.filter(id=instance.id).update(Attributes=pomp_json)
    return True
