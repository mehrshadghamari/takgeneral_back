import math

from django.core.paginator import Paginator
from django.db.models import F
from django.db.models import Q
from extention.models import Blog
from extention.models import Content
from extention.models import HomeBanner
from extention.models import HomeMainBanner
from extention.models import PopularHomeCategory
from extention.models import Redirect
from extention.serializers import AllBlogSerializer
from extention.serializers import BlogSerializer
from extention.serializers import BlogSiteMapSerializer
from extention.serializers import BrandSiteMapSerializer
from extention.serializers import CategorySiteMapSerializer
from extention.serializers import ContentSerializer
from extention.serializers import HomeBannerSerializer
from extention.serializers import HomeMainBannerSerializer
from extention.serializers import MetaTagSerializer
from extention.serializers import PopularHomeCategorySerializer
from extention.serializers import ProductSiteMapSerializer
from extention.serializers import RedirectSerializer
from extention.serializers import SiteMapSerializer
from product.models import Category
from product.models import Product
from product.models import ProductBrand
from product.serializers import AllProductSerializer
from product.serializers import CategorySerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404


class HomeApi(APIView):
    def get(self, request):
        main_banners = HomeMainBanner.objects.all()
        main_banners_serializer = HomeMainBannerSerializer(main_banners, many=True, context={"request": request})

        mid_banners = HomeBanner.objects.filter(place="mid")
        mid_banners_serializer = HomeBannerSerializer(mid_banners, many=True, context={"request": request})

        end_banners = HomeBanner.objects.filter(place="end")
        end_banners_serializer = HomeBannerSerializer(end_banners, many=True, context={"request": request})

        mother_categories = Category.objects.filter(parent=None)
        mother_categories_serializer = CategorySerializer(mother_categories, many=True, context={"request": request})

        popular_categories = PopularHomeCategory.objects.all()
        popular_categories_serializer = PopularHomeCategorySerializer(
            popular_categories, many=True, context={"request": request})

        special_offer_products = Product.objects.filter(special_offer=True).order_by('?')[:20]
        special_offer_serializer = AllProductSerializer(
            special_offer_products, many=True, context={"request": request})

        amazing_offer_product = Product.objects.with_price_info().annotate(
            ekhtelaf=F('lowest_price_manager') - F('lowest_final_price_manager')).filter(
            Q(ekhtelaf__gte=1000000) | Q(highest_discount_manager__gte=1)).order_by('?')[:20]
        amazing_offer_serializer = AllProductSerializer(
            amazing_offer_product, many=True, context={"request": request})

        new_blog = Blog.objects.order_by('-created_time')[:3]
        new_blog_serializer = AllBlogSerializer(
            new_blog, many=True, context={"request": request})

        return Response({
            'main_banner': main_banners_serializer.data,
            'mid_banner': mid_banners_serializer.data,
            'end_banner': end_banners_serializer.data,
            'mother_categories': mother_categories_serializer.data,
            'popular_categories': popular_categories_serializer.data,
            'special_offer_products': special_offer_serializer.data,
            'amazing_offer_product': amazing_offer_serializer.data,
            'new_blogs': new_blog_serializer.data},
            status=status.HTTP_200_OK)


class contentAPI(APIView):
    def get(self, request):
        advertisement = Content.objects.all()
        advertisement_serializer = ContentSerializer(
            advertisement, many=True, )
        return Response(advertisement_serializer.data, status=status.HTTP_200_OK)


class BlogsApi(APIView):
    def get(self, request):
        page_number = self.request.query_params.get('page', 1)
        page_size = self.request.query_params.get('page_size', 20)
        blogs = Blog.objects.all()
        paginator = Paginator(blogs, page_size)
        blogs_serializer = AllBlogSerializer(paginator.page(
            page_number), many=True, context={"request": request})

        page_count = math.ceil(blogs.count() / int(page_size))

        return Response({'current_page': int(page_number),
                         'page_count': page_count,
                         'blogs': blogs_serializer.data, }
                        , status=status.HTTP_200_OK)


class BlogDetail(APIView):
    def get(self, request, slug):
        blog = get_object_or_404(Blog,slug=slug)
        blog_serializer = BlogSerializer(
            blog, context={"request": request})
        meta_tag = blog.meta_tag.first()
        meta_tag_serializer = MetaTagSerializer(meta_tag,context={"request": request})
        return Response({'blog':blog_serializer.data,
                         'meta_tag':meta_tag_serializer.data
                         }, status=status.HTTP_200_OK)


class RedirectView(APIView):
    def get(self , request):
        result = Redirect.objects.all()
        result_serializer = RedirectSerializer(result , many=True) ;
        return Response(result_serializer.data , status = status.HTTP_200_OK)


class SiteMapApi(APIView):
    def get(self,request):
        blogs = Blog.objects.all()
        products = Product.objects.all()
        brands = ProductBrand.objects.all()
        categories = Category.objects.all()
        sitemap_data = {
            'products': products,
            'brands': brands,
            'categories': categories,
            'blogs': blogs,
        }
        sitemap_serializer=SiteMapSerializer(sitemap_data)
        return Response(sitemap_serializer.data,status=status.HTTP_200_OK)
