from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from .models import Attribute
from .models import Category
from .models import Product
from .models import ProductBrand
from .models import ProductCategory
from .models import ProductImage
from .models import ProductSpecification
from .models import ProductSpecificationValue
from .models import ProductType
from .models import TitleAttribute

# Register your models here.


# admin.site.register(HomePomp)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(ProductBrand)
admin.site.register(ProductCategory)
admin.site.register(Attribute)
admin.site.register(TitleAttribute)


###################release 2 admin

# admin.site.register(Category,MPTTModelAdmin)

# class ProductSpecificationInline(admin.TabularInline):
#     model= ProductSpecification



# @admin.register(ProductType)
# class ProductTypeAdmin(admin.ModelAdmin):
#     inlines=[ProductSpecificationInline,]


# class ProductImageInline(admin.TabularInline):
#     model=ProductImage


# class ProductSpecificationValueInline(admin.TabularInline):
#     model=ProductSpecificationValue



# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     inlines=[
#         ProductImageInline,
#         ProductSpecificationValueInline,
#     ]
