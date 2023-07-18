from django import forms
from django.contrib import admin
from extention.admin import ContentInline
from mptt.admin import MPTTModelAdmin

# from .models import ProductCategory
# from .models import Attribute
from .models import Category
from .models import Product
from .models import ProductBrand
from .models import ProductImage
from .models import ProductSpecification
from .models import ProductSpecificationValue
from .models import ProductType

# from .models import TitleAttribute

# Register your models here.


# admin.site.register(HomePomp)
# admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(ProductBrand)
# admin.site.register(ProductCategory)
# admin.site.register(Attribute)
# admin.site.register(TitleAttribute)


###################release 2 admin

# class ProductAdminForm(forms.ModelForm):
#     class Meta:
#         model = Product
#         fields = '__all__'

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # Filter the ProductSpecificationValueInline based on the selected ProductType
#         product_type = self.instance.product_type
#         if product_type:
#             self.fields['productspecificationvalue_set'].queryset = ProductSpecificationValue.objects.filter(
#                 product=self.instance
#             )

admin.site.register(Category,MPTTModelAdmin)

class ProductSpecificationInline(admin.TabularInline):
    model= ProductSpecification



@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    inlines=[ProductSpecificationInline,]


class ProductImageInline(admin.TabularInline):
    model=ProductImage




# class ProductSpecificationValueInline(admin.TabularInline):
#     model = ProductSpecificationValue


# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     # form = ProductAdminForm
#     inlines=[
#         ProductImageInline,
#         ProductSpecificationValueInline,
#     ]


class ProductSpecificationValueInline(admin.TabularInline):
    model = ProductSpecificationValue


    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['product_type'].widget.can_add_related = False
        return form

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'product':
            kwargs['queryset'] = Product.objects.all()
        if db_field.name == 'specification':
            product_type_id = request.POST.get('product_type', None)
            if product_type_id:
                kwargs['queryset'] = ProductSpecification.objects.filter(
                    id=product_type_id
                )
            else:
                kwargs['queryset'] = ProductSpecification.objects.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # ...

    inlines = [
        ProductImageInline,
        ProductSpecificationValueInline,
        ContentInline,
    ]

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['product_type'].widget.can_add_related = False
        return form
