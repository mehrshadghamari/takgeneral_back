from django import forms
from django.contrib import admin
from django.forms import BaseInlineFormSet
from django.utils.translation import get_language_bidi
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy
from extention.admin import BannerInline
from extention.admin import ContentImageInline
from extention.admin import ContentInline
from extention.admin import MainBannerInline
from extention.admin import MetaTagInline
from mptt.admin import MPTTModelAdmin
from nested_inline.admin import NestedModelAdmin
from nested_inline.admin import NestedTabularInline

from .models import Category
from .models import Product
from .models import ProductBrand
from .models import ProductImage
from .models import ProductSpecification
from .models import ProductSpecificationValue
from .models import ProductType

# Register your models here.



# form

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


# inlines


class ProductSpecificationInline(admin.TabularInline):
    search_fields = ['name',]
    model= ProductSpecification




class ProductImageInline(admin.TabularInline):
    model=ProductImage





# class FilterOptionTypeInline(NestedTabularInline):
#     model=FilterOptionType
#     extra=1



# class FilterOptionInline(NestedTabularInline):
#     model=FilterOption
#     extra=1


# admin.site.register(FilterOptionType)




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




# admin

@admin.register(ProductBrand)
class ProductBrandAdmin(NestedModelAdmin):
    search_fields = ['name',]
    inlines=[ContentInline,MainBannerInline,BannerInline,MetaTagInline]



@admin.register(Category)
class CategotyAdmin(NestedModelAdmin,MPTTModelAdmin):
    search_fields = ['name',]
    inlines=[ContentInline,MainBannerInline,BannerInline,MetaTagInline,]




@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    search_fields = ['name',]
    inlines=[ProductSpecificationInline,]





@admin.register(Product)
class ProductAdmin(NestedModelAdmin):
    form = ProductForm
    autocomplete_fields = ("brand","product_type",)
    inlines = [
        ProductImageInline,
        ProductSpecificationValueInline,
        ContentInline,
        MetaTagInline,
    ]

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['product_type'].widget.can_add_related = False
        return form


    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "category":
            # Filter the category field's queryset to show only leaf nodes
            kwargs["queryset"] = Category.objects.filter(children__isnull=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
