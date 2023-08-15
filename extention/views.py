from django.db.models import F
from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from extention.models import Blog
from extention.models import Content
from extention.models import HomeBanner
from extention.models import HomeMainBanner
from extention.serializers import AllBlogSerializer
from extention.serializers import BlogSerializer
from extention.serializers import ContentSerializer
from extention.serializers import HomeBannerSerializer
from extention.serializers import HomeMainBannerSerializer
from product.models import Category
from product.models import Product
from product.serializers import AllProductSerializer
from product.serializers import CategorySerializer


# class HomeApi(APIView):
#     def get(self, request):
#         special_offer_products = Product.objects.filter(special_offer=True)
#         special_offer_serializer = AllProductSerializer(
#             special_offer_products, many=True, context={"request": request})
#         # amazing_offer_product=Product.objects.filter(discount__gte=20)
#         amazing_offer_product = Product.objects.with_final_price().annotate(ekhtelaf=F(
#             'price') - F('final_price_Manager')).filter(Q(ekhtelaf__gte=1000000) | Q(discount__gte=20))
#         # amazing_offer_product=Product.objects.annotate(final_price=F('price')-(F('price')*F('discount')/100)).annotate(ekhtelaf=F('price') - F('final_price')).filter(ekhtelaf__gte=1000000)
#         # amazing_offer_product=Product.objects.annotate(ekhtelaf=F('price') - F('final_price')).filter(ekhtelaf__gte=1000000)
#         amazing_offer_serializer = AllProductSerializer(
#             amazing_offer_product, many=True, context={"request": request})
#         return Response({'special_offer_products': special_offer_serializer.data,
#                          'amazing_offer_product': amazing_offer_serializer.data}, status=status.HTTP_200_OK)


class HomeApi(APIView):
    def get(self, request):
        main_banners = HomeMainBanner.objects.all()
        main_banners_serializer = HomeMainBannerSerializer(main_banners, many=True, context={"request": request})
        mid_banners = HomeBanner.objects.filter(place="mid")
        mid_banners_serializer = HomeBannerSerializer(mid_banners, many=True, context={"request": request})
        end_banners = HomeBanner.objects.filter(place="end")
        end_banners_serializer = HomeBannerSerializer(end_banners, many=True, context={"request": request})
        mother_category = Category.objects.filter(parrent=None)
        mother_category_serializer = CategorySerializer(mother_category, many=True)
        special_offer_products = Product.objects.filter(special_offer=True)
        special_offer_serializer = AllProductSerializer(
            special_offer_products, many=True, context={"request": request})
        amazing_offer_product = Product.objects.with_price().annotate(ekhtelaf=F(
            'lowest_price') - F('lowest_final_price')).filter(Q(ekhtelaf__gte=1000000) | Q(highest_discount__gte=20))
        amazing_offer_serializer = AllProductSerializer(
            amazing_offer_product, many=True, context={"request": request})
        return Response({
            'main_banner': main_banners_serializer.data,
            'mid_banner': mid_banners_serializer.data,
            'end_banner': end_banners_serializer.data,
            'mother_category': mother_category_serializer.data,
            'special_offer_products': special_offer_serializer.data,
            'amazing_offer_product': amazing_offer_serializer.data},
            status=status.HTTP_200_OK)


class contentAPI(APIView):
    def get(self, request):
        advertisement = Content.objects.all()
        advertisement_serializer = ContentSerializer(
            advertisement, many=True, )
        return Response(advertisement_serializer.data, status=status.HTTP_200_OK)


class BlogsApi(APIView):
    def get(self, request):
        blogs = Blog.objects.all()
        blogs_serializer = AllBlogSerializer(
            blogs, many=True, context={"request": request})
        return Response(blogs_serializer.data, status=status.HTTP_200_OK)


class BlogDetail(APIView):
    def get(self, request, id):
        blog = Blog.objects.get(id=id)
        blog_serializer = BlogSerializer(
            blog, context={"request": request})
        return Response(blog_serializer.data, status=status.HTTP_200_OK)
