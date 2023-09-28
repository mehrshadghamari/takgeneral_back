import math

from django.core.paginator import Paginator
from django.db.models import Avg
from django.db.models import Count
from django.shortcuts import get_object_or_404
from extention.serializers import BannerSAerializer
from extention.serializers import ContentSerializer
from extention.serializers import MainBannerSAerializer
from extention.serializers import MetaTagSerializer
from product.models import ProductBrand
from product_action.models import Comment
from product_action.models import Question
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Category
from .models import Product
from .serializers import AllCategorySerializer
from .serializers import AllProductSerializer
from .serializers import BrandInfoSerializer
from .serializers import BrandSerializer
from .serializers import CategorySerializer
from .serializers import CommentsSerializer
from .serializers import QuestionSerializer
from .serializers import productDetailSerializer


class AllCategoryList(APIView):
    def get(self, request):
        queryset = Category.objects.filter(parent=None)
        serializer = AllCategorySerializer(queryset, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class products(APIView):
    def get(self, request, cat_url):
        category_obj = get_object_or_404(Category, url=cat_url)
        if category_obj.parent is None:
            main_category_serializer = CategorySerializer(category_obj, context={"request": request})
            categories = category_obj.get_children()
            sub_categories_serializer = CategorySerializer(categories, many=True, context={"request": request})
            breadcrumb = category_obj.get_ancestors(include_self=True)
            breadcrumb_serializer = CategorySerializer(breadcrumb, many=True, context={"request": request})
            # brands = Product.objects.filter(category__in=category_obj.get_children()).values('brand__id').annotate(
            #     product_count=Count('brand')).values('brand__id', 'brand__name', 'brand__logo', 'product_count')
            # brands_serializer = BrandInfoSerializer(brands,many=True,context={"request": request})
            brands_ids = Product.objects.select_related('brand').filter(
                category__in=category_obj.get_descendants(include_self=True)).values_list('brand__id', flat=True)
            brand_ids_list = list(set(brands_ids))
            brands = ProductBrand.objects.filter(id__in=brand_ids_list)
            brands_serializer = BrandSerializer(brands, many=True, context={"request": request})
            main_banner = category_obj.main_banners.all()
            main_banner_serializer = MainBannerSAerializer(main_banner, many=True, context={"request": request})
            other_banner = category_obj.banners.all()
            other_banner_serializer = BannerSAerializer(other_banner, many=True, context={"request": request})
            page_content = category_obj.content.first()
            page_content_serializer = ContentSerializer(page_content)
            meta_tag = category_obj.meta_tag.first()
            meta_tag_serializer = MetaTagSerializer(meta_tag,context={"request": request})

            response = Response({
                'breadcrumb': breadcrumb_serializer.data,
                'page_content': page_content_serializer.data,
                'meta_tag': meta_tag_serializer.data,
                'main_banner': main_banner_serializer.data,
                'other_banner': other_banner_serializer.data,
                'brands': brands_serializer.data,
                "main_category": main_category_serializer.data,
                "sub_category": sub_categories_serializer.data},
                status=status.HTTP_200_OK)

        else:
            if category_obj.is_leaf_node():
                main_category_serializer = CategorySerializer(category_obj, context={"request": request})
                sub_categories_serializer = CategorySerializer(category_obj.parent.get_children(), many=True,
                                                               context={"request": request})
                breadcrumb = category_obj.get_ancestors(include_self=True)
                breadcrumb_serializer = CategorySerializer(breadcrumb, many=True, context={"request": request})
                product_query = Product.objects.with_price_info().select_related("brand", "category", ).filter(
                    category=category_obj).order_by('-special_offer', '-created_at')

            else:
                main_category_serializer = CategorySerializer(category_obj, context={"request": request})
                sub_categories_serializer = CategorySerializer(category_obj.get_children(), many=True,
                                                               context={"request": request})
                breadcrumb = category_obj.get_ancestors(include_self=True)
                breadcrumb_serializer = CategorySerializer(breadcrumb, many=True, context={"request": request})
                product_query = Product.objects.with_price_info().select_related("brand", "category").filter(
                    category__in=category_obj.get_descendants(include_self=True)).order_by('-special_offer', '-created_at')

            # brand_query_before = product_query.values('brand__id').annotate(
            #     product_count=Count('brand')).values('brand__id',)
            brand_count_query = Product.objects.filter(id__in=product_query.values('id')).values('brand__id').annotate(
                product_count=Count(
                    'brand')).values('brand__id', 'brand__name', 'product_count')

            min_price = self.request.query_params.get('min_price', None)
            max_price = self.request.query_params.get('max_price', None)
            if min_price and max_price:
                product_query = product_query.filter(final_price_Manager__gte=int(
                    min_price), final_price_Manager__lte=int(max_price))
                # brand_query_before = product_query.values('brand__id').annotate(
                #     product_count=Count('brand')).values('brand__id')
                brand_count_query = Product.objects.filter(id__in=product_query.values('id')).values('brand__id').annotate(
                product_count=Count(
                    'brand')).values('brand__id', 'brand__name', 'product_count')

            # brand_query = brand_query_before

            brand = self.request.query_params.getlist('brand[]')
            if brand:
                product_query = product_query.filter(brand__id__in=brand)
            else:
                # brand_query = product_query.values('brand__id').annotate(product_count=Count(
                #     'brand')).values('brand__id')
                brand_count_query = Product.objects.filter(id__in=product_query.values('id')).values('brand__id').annotate(
                product_count=Count(
                    'brand')).values('brand__id', 'brand__name', 'product_count')

            ordering = self.request.query_params.get('ordering', None)
            if ordering is not None:
                if ordering == 'price':
                    product_query = product_query.order_by('lowest_final_price_manager')
                elif ordering == '-price':
                    product_query = product_query.order_by('-lowest_final_price_manager')

            page_number = self.request.query_params.get('page', 1)
            # page_size = 20
            page_size = self.request.query_params.get('page_size', 20)

            paginator = Paginator(product_query, page_size)

            product_serializer = AllProductSerializer(paginator.page(
                page_number), many=True, context={"request": request})

            page_count = math.ceil(product_query.count() / int(page_size))

            main_banner = category_obj.main_banners.all()
            main_banner_serializer = MainBannerSAerializer(main_banner, many=True, context={"request": request})
            other_banner = category_obj.banners.all()
            other_banner_serializer = BannerSAerializer(other_banner, many=True, context={"request": request})
            page_content = category_obj.content.first()
            page_content_serializer = ContentSerializer(page_content)
            meta_tag = category_obj.meta_tag.first()
            meta_tag_serializer = MetaTagSerializer(meta_tag,context={"request": request})

            # included_brand_ids = set()

            # brands = []

            # # Loop through the brand data
            # for brand_data in brand_query:
            #     brand_id = brand_data['brand__id']
            #     # Check if the brand ID has already been included in the response
            #     if brand_id not in included_brand_ids:
            #         included_brand_ids.add(brand_id)  # Add the brand ID to the set
            #         brands.append(brand_data)
            

            # brand_count_query = Product.objects.filter(id__in=product_query.values('id')).values('brand__id').annotate(
            #     product_count=Count(
            #         'brand')).values('brand__id', 'brand__name', 'product_count')

            brands_info = ProductBrand.objects.filter(id__in=brand_count_query.values('brand__id'))
            brand_count_map = {item['brand__id']: item['product_count'] for item in brand_count_query}

            combined_data = []

            # Iterate over the brands_info queryset
            for brand_info in brands_info:
                brand_id = brand_info.id
                product_count = brand_count_map.get(brand_id, 0)  # Get the product count from the map

                # Create a new dictionary with the combined data
                combined_brand_info = {
                    'id': brand_id,
                    'name': brand_info.name,
                    'logo': brand_info.logo.url if brand_info.logo else "",
                    'product_count': product_count,
                }

                combined_data.append(combined_brand_info)

            brands_serializer = BrandInfoSerializer(combined_data, many=True, context={"request": request})

            response = Response({
                'breadcrumb': breadcrumb_serializer.data,
                'page_content': page_content_serializer.data,
                'meta_tag': meta_tag_serializer.data,
                'main_banner': main_banner_serializer.data,
                'other_banner': other_banner_serializer.data,
                'current_page': int(page_number),
                'page_count': page_count,
                "main_category": main_category_serializer.data,
                "sub_category": sub_categories_serializer.data,
                'product': product_serializer.data,
                'brands': brands_serializer.data},
                status=status.HTTP_200_OK)

        return response


class Brands(APIView):
    def get(self, request, brand_url):
        brand_obj = get_object_or_404(ProductBrand, url=brand_url)
        brand_serializer = BrandSerializer(brand_obj, context={"request": request})
        main_banner = brand_obj.main_banners.all()
        main_banner_serializer = MainBannerSAerializer(main_banner, many=True, context={"request": request})
        other_banner = brand_obj.banners.all()
        other_banner_serializer = BannerSAerializer(other_banner, many=True, context={"request": request})
        page_content = brand_obj.content.first()
        page_content_serializer = ContentSerializer(page_content)
        product_query = Product.objects.with_price_info().select_related("brand", "category").filter(
            brand=brand_obj).order_by('-special_offer', '-created_at')
        meta_tag = brand_obj.meta_tag.first()
        meta_tag_serializer = MetaTagSerializer(meta_tag,context={"request": request})
        # default page number = 1
        page_number = self.request.query_params.get('page', 1)
        # default page_size = 20
        page_size = self.request.query_params.get('page_size', 20)

        ordering = self.request.query_params.get('ordering', None)
        if ordering is not None:
            if ordering == 'price':
                product_query = product_query.order_by('lowest_final_price_manager')
            elif ordering == '-price':
                product_query = product_query.order_by('-lowest_final_price_manager')

        paginator = Paginator(product_query, page_size)

        product_serializer = AllProductSerializer(paginator.page(
            page_number), many=True, context={"request": request})

        page_count = math.ceil(product_query.count() / int(page_size))

        return Response({
            'page_content': page_content_serializer.data,
            'meta_tag': meta_tag_serializer.data,
            'main_banner': main_banner_serializer.data,
            'other_banner': other_banner_serializer.data,
            'current_page': int(page_number),
            'page_count': page_count,
            'brand': brand_serializer.data,
            'products': product_serializer.data, },
            status=status.HTTP_200_OK)


class ProductDetail(APIView):
    def get(self, request, id):
        product_instance = get_object_or_404(Product, id=id)
        product_serializer = productDetailSerializer(
            product_instance, context={"request": request})
        breadcrumb = product_instance.category.get_ancestors(include_self=True)
        breadcrumb_serializer = CategorySerializer(breadcrumb, many=True, context={"request": request})
        comments = Comment.objects.filter(product__id=id).order_by('-created_at')
        comments_serializer = CommentsSerializer(comments, many=True)
        questions = Question.objects.filter(product__id=id).order_by('-created_at')
        questions_serializer = QuestionSerializer(questions, many=True)

        # Retrieve similar products based on price and category
        similar_product = Product.objects.filter(id__in=product_instance.similar_product_ids,
                                                 category=product_instance.category)

        similar_product_serializer = AllProductSerializer(
            similar_product, context={"request": request}, many=True)

        avg = comments.aggregate(avg_rate=Avg('rate'))

        page_content = product_instance.content.first()
        page_content_serializer = ContentSerializer(page_content)
        meta_tag = product_instance.meta_tag.first()
        meta_tag_serializer = MetaTagSerializer(meta_tag,context={"request": request})

        return Response({
            'breadcrumb': breadcrumb_serializer.data,
            'product': product_serializer.data,
            'comments': comments_serializer.data,
            'questions': questions_serializer.data,
            'avg_rate': avg,
            'similar_product': similar_product_serializer.data,
            'page_content': page_content_serializer.data,
            'meta_tag': meta_tag_serializer.data,
        }, status=status.HTTP_200_OK)
