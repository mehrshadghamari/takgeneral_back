from rest_framework import serializers

from product_action.models import Comment
from product_action.models import Question
from product_action.models import Reply
from .models import Category
from .models import Product
from .models import ProductBrand
from .models import ProductImage
from .models import ProductOptionType
from .models import ProductSpecificationValue
from .models import ProductVariant
from extention.serializers import BannerSerializer
from extention.serializers import ContentSerializer
from extention.serializers import MainBannerSerializer
from extention.serializers import MetaTagSerializer


class AttributeSerializer(serializers.ModelSerializer):
    specification = serializers.SerializerMethodField("get_specification")

    def get_specification(self, obj):
        return obj.specification.name

    class Meta:
        model = ProductSpecificationValue
        fields = ("specification", "value")


class productImagesSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField('get_image_url')

    def get_image_url(self, obj):
        request = self.context.get('request')
        image_url = obj.image.url
        return request.build_absolute_uri(image_url)

    class Meta:
        model = ProductImage
        exclude = ("created_at", "upload_at", "product")


class CommentsSerializer(serializers.ModelSerializer):
    diss_likes_count = serializers.IntegerField()
    likes_count = serializers.IntegerField()
    created_at = serializers.SerializerMethodField()

    def get_created_at(self, obj):
        return {'date': obj.created_at.strftime('%Y-%m-%d'), 'time': obj.created_at.strftime('%H:%M:%S'),
                'timestamp': int(obj.created_at.timestamp())}

    class Meta:
        model = Comment
        fields = ('id', 'user_alias_name', 'title', 'content', 'likes_count',
                  'diss_likes_count', 'suggest_me', 'arzesh_rate', 'kefiyat_rate', 'created_at')


class ReplySerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()

    def get_created_at(self, obj):
        return {'date': obj.created_at.strftime('%Y-%m-%d'), 'time': obj.created_at.strftime('%H:%M:%S'),
                'timestamp': int(obj.created_at.timestamp())}

    class Meta:
        model = Reply
        fields = ('id', 'user', 'content', 'created_at')


class QuestionSerializer(serializers.ModelSerializer):
    replys = ReplySerializer(many=True)
    created_at = serializers.SerializerMethodField()

    def get_created_at(self, obj):
        return {'date': obj.created_at.strftime('%Y-%m-%d'), 'time': obj.created_at.strftime('%H:%M:%S'),
                'timestamp': int(obj.created_at.timestamp())}

    class Meta:
        model = Question
        fields = ('id', 'user', 'content', 'created_at', 'replys')


class ProductVariantSerializer(serializers.ModelSerializer):
    final_price = serializers.FloatField()
    product_available = serializers.BooleanField()
    warranty = serializers.CharField()

    class Meta:
        model = ProductVariant
        exclude = ('option', 'Inventory_number', 'waranty_tamir',
                   'waranty_taviz', 'month_of_waranty',)


class ProductOptionTypeSerializer(serializers.ModelSerializer):
    product_variant = ProductVariantSerializer(many=True)

    class Meta:
        model = ProductOptionType
        fields = ("id", "no_option", "name", "product_variant")


class productDetailSerializer(serializers.ModelSerializer):
    attributes = AttributeSerializer(many=True)
    all_images = productImagesSerializer(many=True)
    brand = serializers.SerializerMethodField('get_brand')
    options = ProductOptionTypeSerializer()

    # pdf = serializers.SerializerMethodField("get_pdf_url")

    # def get_pdf_url(self, obj):
    #     request = self.context.get('request')
    #     pdf_url = obj.pdf.url
    #     return request.build_absolute_uri(pdf_url)

    def get_brand(self, obj):
        return obj.brand.name

    class Meta:
        model = Product
        fields = '__all__'


class ProductVariantPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = ("price", "final_price", "discount")


class AllProductSerializer(serializers.ModelSerializer):
    brand = serializers.SerializerMethodField('get_brand')
    main_image = productImagesSerializer()
    min_price = ProductVariantPriceSerializer()

    def get_brand(self, obj):
        return obj.brand.name

    class Meta:
        model = Product
        fields = ('id', 'url', 'main_image', 'name', 'min_price', 'brand', 'special_offer')


class productCountFromSpecificBrand(serializers.ModelSerializer):
    product_count = serializers.IntegerField()

    class Meta:
        model = ProductBrand
        fields = ('id', 'name', 'product_count',)


class AllCategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    def get_children(self, obj):
        children = obj.children.all()
        serializer = self.__class__(children, many=True)
        return serializer.data

    class Meta:
        model = Category
        fields = ['id', 'name', 'url', 'parent', 'is_active', 'children']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'url', 'parent', 'is_active', ]


class BrandSerializer(serializers.ModelSerializer):
    logo = serializers.SerializerMethodField("get_logo_url")

    def get_logo_url(self, obj):
        request = self.context.get('request')
        logo = obj.logo
        if logo and logo.url:
            return request.build_absolute_uri(logo.url)
        return None

    class Meta:
        model = ProductBrand
        fields = ['id', 'name', 'logo', 'url', ]

# class FilterOptionSerializer(serializers.ModelSerializer):
#     filter_option_type = serializers.SerializerMethodField("get_filter_option_type")

#     def get_filter_option_type(self,obj):
#         return obj.filter_option_type.get_options

#     class Meta:
#         model = FilterOption
#         fields = ['specification_name', 'filter_option_type', 'min_value', 'max_value',]



class BrandPageSerializer(serializers.Serializer):
    page_content = ContentSerializer()
    meta_tag = MetaTagSerializer()
    main_banner = MainBannerSerializer(many=True)
    other_banner = BannerSerializer(many=True)
    current_page = serializers.IntegerField()
    page_count = serializers.IntegerField()
    brand = BrandSerializer()
    products = AllProductSerializer(many=True)