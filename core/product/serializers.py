from datetime import datetime

from product_action.models import Comment
from product_action.models import Question
from product_action.models import Reply
from rest_framework import serializers

from .models import Category
from .models import Product
from .models import ProductBrand
from .models import ProductImage
from .models import ProductSpecification
from .models import ProductSpecificationValue


class AttributeSerilizer(serializers.ModelSerializer):
    specification = serializers.SerializerMethodField("get_specification")

    def get_specification(self,obj):
        return obj.specification.name

    class Meta:
        model = ProductSpecificationValue
        fields=("specification","value")


class productImaagesSerilizer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        exclude= ("created_at","upload_at","product")


class CommentsSerializer(serializers.ModelSerializer):
    diss_likes_count = serializers.IntegerField()
    likes_count = serializers.IntegerField()
    created_at = serializers.SerializerMethodField()

    def get_created_at(self, obj):
        return {'date': obj.created_at.strftime('%Y-%m-%d'), 'time': obj.created_at.strftime('%H:%M:%S'), 'timestamp': int(obj.created_at.timestamp())}

    class Meta:
        model = Comment
        fields = ('id', 'user_alias_name', 'title', 'content', 'likes_count',
                  'diss_likes_count', 'suggest_me', 'arzesh_rate', 'kefiyat_rate', 'created_at')


class ReplySerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()

    def get_created_at(self, obj):
        return {'date': obj.created_at.strftime('%Y-%m-%d'), 'time': obj.created_at.strftime('%H:%M:%S'), 'timestamp': int(obj.created_at.timestamp())}

    class Meta:
        model = Reply
        fields = ('id', 'user', 'content', 'created_at')


class QuestionSerializer(serializers.ModelSerializer):
    replys = ReplySerializer(many=True)
    created_at = serializers.SerializerMethodField()

    def get_created_at(self, obj):
        return {'date': obj.created_at.strftime('%Y-%m-%d'), 'time': obj.created_at.strftime('%H:%M:%S'), 'timestamp': int(obj.created_at.timestamp())}

    class Meta:
        model = Question
        fields = ('id', 'user', 'content', 'created_at', 'replys')



class productDetailSerializer(serializers.ModelSerializer):

    attributes = AttributeSerilizer(many=True)
    all_images = productImaagesSerilizer(many=True)

    brand = serializers.SerializerMethodField('get_brand')
    final_price = serializers.FloatField()
    product_available = serializers.BooleanField()
    warranty = serializers.CharField()

    class Meta:
        model = Product
        # fields='__all__'
        exclude = ('count_of_product', 'waranty_tamir',
                   'waranty_taviz', 'month_of_waranty',)

    def get_brand(self, obj):
        return obj.brand.name


class AllProductSerializer(serializers.ModelSerializer):
    brand = serializers.SerializerMethodField('get_brand')
    main_image = productImaagesSerilizer()


    class Meta:
        model = Product
        fields = ('id','main_image', 'name', 'price',
                  'final_price', 'discount', 'brand',)

    def get_brand(self, obj):
        return obj.brand.name


class ProductIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id',)


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
        fields = ['id', 'name', 'slug', 'parent', 'is_active', 'children']


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'parent', 'is_active',]



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
        fields = ['id', 'name', 'logo', 'url',]
