from django import forms
from django.contrib import admin
from django.forms import BaseInlineFormSet
from extention.admin import ContentInline,ContentImageInline,MainBannerInline,BannerInline
from mptt.admin import MPTTModelAdmin
from nested_inline.admin import NestedModelAdmin

from .models import Category
from .models import Product
from .models import ProductBrand
from .models import ProductImage
from .models import ProductSpecification
from .models import ProductSpecificationValue
from .models import ProductType
from django.utils.translation import get_language_bidi, gettext as _, gettext_lazy
# Register your models here.



@admin.register(ProductBrand)
class ProductBrandAdmin(NestedModelAdmin):
    inlines=[ContentInline,MainBannerInline,BannerInline]




# admin.site.register(Category,MPTTModelAdmin)
@admin.register(Category)
class CategotyAdmin(NestedModelAdmin,MPTTModelAdmin):
    inlines=[ContentInline,MainBannerInline,BannerInline]



class ProductSpecificationInline(admin.TabularInline):
    model= ProductSpecification



@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    inlines=[ProductSpecificationInline,]


class ProductImageInline(admin.TabularInline):
    model=ProductImage







# class ProductSpecificationValueInline(admin.TabularInline):
#     model = ProductSpecificationValue

#     def formfield_for_foreignkey(self, db_field, request, **kwargs):
#         if db_field.name == 'specification':
#             product_id = request.resolver_match.kwargs.get('object_id')
#             if product_id:
#                 product = Product.objects.get(pk=product_id)
#                 kwargs['queryset'] = ProductSpecification.objects.filter(product_type=product.product_type)
#             else:
#                 kwargs['queryset'] = ProductSpecification.objects.all()
#         return super().formfield_for_foreignkey(db_field, request, **kwargs)






class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        product_type = cleaned_data.get('product_type')
        if not product_type:
            raise forms.ValidationError("A product type must be selected.")
        return cleaned_data


class ProductSpecificationValueInline(admin.TabularInline):
    model = ProductSpecificationValue

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'specification':
            product_id = request.resolver_match.kwargs.get('object_id')
            if product_id:
                product = Product.objects.get(pk=product_id)
                kwargs['queryset'] = ProductSpecification.objects.filter(product_type=product.product_type)
            else:
                kwargs['queryset'] = ProductSpecification.objects.none()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)






@admin.register(Product)
class ProductAdmin(NestedModelAdmin):
    # ...
    form = ProductForm
    inlines = [
        ProductImageInline,
        ProductSpecificationValueInline,
        ContentInline,
        # ContentImageInline,
    ]

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['product_type'].widget.can_add_related = False
        return form
