from django.contrib import admin

from .models import Product,ProductBrand,ProductCategory,ProductImage,Attribute,TitleAttribute
# Register your models here.


# admin.site.register(HomePomp)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(ProductBrand)
admin.site.register(ProductCategory)
admin.site.register(Attribute)
admin.site.register(TitleAttribute)