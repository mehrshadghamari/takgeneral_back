from rest_framework import serializers
from .models import Product, ProductCategory, Attribute, ProductImage, ProductBrand
from product_action.models import Comment


# class HomePompDetailSerializer(serializers.ModelSerializer):
#
# brand=serializers.SerializerMethodField('get_brand')
# main_image=serializers.SerializerMethodField('get_main_image')
# final_price=serializers.IntegerField()
# pomp_available=serializers.BooleanField()
#
#
#
# class Meta:
# model=HomePomp
# fields='__all__'
#
# def get_brand(self,obj):
# return obj.name
#
# def get_main_image(self, obj):
# request = self.context.get('request')
# main_image_url = obj.main_image.url
# return request.build_absolute_uri(main_image_url)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = '__all__'


class AttributeSerilizer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField('get_title')

    class Meta:
        model = Attribute
        fields = ('id', 'title', 'value',)

    def get_title(self, obj):
        return obj.title.name


class productImaagesSerilizer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'



class CommentsSerializer(serializers.ModelSerializer):
    diss_likes_count=serializers.IntegerField()
    likes_count=serializers.IntegerField()

    class Meta:
        model = Comment
        fields = ('user_alias_name', 'content','likes_count','diss_likes_count', 'suggest_me','arzesh_rate', 'kefiyat_rate', 'created_at')



class productDetailSerializer(serializers.ModelSerializer):

    category = CategorySerializer(many=True)
    attributes = AttributeSerilizer(many=True)
    other_images = productImaagesSerilizer(many=True)

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

    class Meta:
        model = Product
        fields = ('id', 'name', 'main_image', 'price',
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
