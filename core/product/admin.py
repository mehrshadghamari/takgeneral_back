from django.contrib import admin

from .models import Attribute
from .models import Product
from .models import ProductBrand
from .models import ProductCategory
from .models import ProductImage
from .models import TitleAttribute

# Register your models here.


# admin.site.register(HomePomp)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(ProductBrand)
admin.site.register(ProductCategory)
admin.site.register(Attribute)
admin.site.register(TitleAttribute)
