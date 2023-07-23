import math

from django.core.paginator import Paginator
from django.db.models import Avg
from django.db.models import Count
from django.shortcuts import get_object_or_404
from extention.models import Banner
from extention.models import Content
from extention.models import MainBanner
from extention.serializers import BannerSAerializer
from extention.serializers import ContentSerializer
from extention.serializers import MainBannerSAerializer
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
from .serializers import BrandSerializer
from .serializers import CategorySerializer
from .serializers import CommentsSerializer
from .serializers import ProductIDSerializer
from .serializers import QuestionSerializer
from .serializers import productDetailSerializer


class Brands(APIView):
    def get(self,request,brand_id):
        brand_obj= ProductBrand.objects.filter(id=brand_id).first()
        brand_serializer = BrandSerializer(brand_obj,context={"request": request})
        main_banner = brand_obj.mainbanner_set.all()
        main_banner_serializer = MainBannerSAerializer(main_banner,many=True,context={"request": request})
        other_banner = brand_obj.banner_set.all()
        other_banner_serializer = BannerSAerializer(other_banner,many=True,context={"request": request})
        page_content= Content.objects.filter(brand=brand_obj).first()
        page_content_serializer = ContentSerializer(page_content)
        product_query = Product.objects.filter(brand=brand_obj)
        #default page number = 1
        page_number = self.request.query_params.get('page', 1)
        #default page_size = 20
        page_size = self.request.query_params.get('page_size', 20)

        paginator = Paginator(product_query, page_size)

        product_serializer = AllProductSerializer(paginator.page(
                page_number), many=True, context={"request": request})

        page_count = math.ceil(product_query.count()/int(page_size))

        return Response({
                            'page_content':page_content_serializer.data,
                            'main_banner':main_banner_serializer.data,
                            'other_banner':other_banner_serializer.data,
                            'current_page': int(page_number),
                            'page_count': page_count,
                            'brand':brand_serializer.data,
                            'products':product_serializer.data,},
                            status=status.HTTP_200_OK)



class  AllCategoryList(APIView):
    def get(self,request):
        queryset = Category.objects.filter(parent=None)
        serializer = AllCategorySerializer(queryset,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)



class products(APIView):
    def get(self, request,cat_id):

        category_obj=Category.objects.get(id=cat_id)
        if category_obj.parent ==None:
            main_category_serilizer = CategorySerializer(category_obj)
            categories = category_obj.get_children()
            sub_categories_serilizer = CategorySerializer(categories,many=True)
            brands= Product.objects.values('brand__id').annotate(
                product_count=Count('brand')).values('brand__id', 'brand__name','brand__logo', 'product_count')
            main_banner = category_obj.mainbanner_set.all()
            main_banner_serializer = MainBannerSAerializer(main_banner,many=True,context={"request": request})
            other_banner = category_obj.banner_set.all()
            other_banner_serializer = BannerSAerializer(other_banner,many=True,context={"request": request})
            page_content= Content.objects.filter(category=category_obj).first()
            page_content_serializer = ContentSerializer(page_content)
            return Response({
                            'page_content':page_content_serializer.data,
                            'main_banner':main_banner_serializer.data,
                            'other_banner':other_banner_serializer.data,
                            'brands':brands,
                            "main_category":main_category_serilizer.data,
                            "sub_category":sub_categories_serilizer.data},
                            status=status.HTTP_200_OK)

        else :
            if category_obj.is_leaf_node():
                main_category_serilizer= CategorySerializer(category_obj.parent)
                sub_categories_serilizer = CategorySerializer(category_obj.parent.get_children(),many=True)

            else:
                main_category_serilizer= CategorySerializer(category_obj)
                sub_categories_serilizer = CategorySerializer(category_obj.get_children(),many=True)


            product_query = Product.objects.with_final_price().filter(
                category=category_obj).order_by('-created_at')

            brand_query_before = product_query.values('brand__id').annotate(
                product_count=Count('brand')).values('brand__id', 'brand__name', 'product_count')

            min_price = self.request.query_params.get('min_price', None)
            max_price = self.request.query_params.get('max_price', None)
            if min_price and max_price:
                product_query = product_query.filter(final_price_Manager__gte=int(
                    min_price), final_price_Manager__lte=int(max_price))
                brand_query_before = product_query.values('brand__id').annotate(
                    product_count=Count('brand')).values('brand__id', 'brand__name', 'product_count')

            brand_query = brand_query_before

            brand = self.request.query_params.getlist('brand[]')
            if brand:
                product_query = product_query.filter(brand__id__in=brand)
            else:
                brand_query = product_query.values('brand__id').annotate(product_count=Count(
                    'brand')).values('brand__id', 'brand__name', 'product_count')

            ordering = self.request.query_params.get('ordering', None)
            if ordering is not None:
                if ordering == 'price':
                    product_query = product_query.order_by('final_price_Manager')
                elif ordering == '-price':
                    product_query = product_query.order_by('-final_price_Manager')

            page_number = self.request.query_params.get('page', 1)
            # page_size = 20
            page_size = self.request.query_params.get('page_size', 20)

            paginator = Paginator(product_query, page_size)

            product_serializer = AllProductSerializer(paginator.page(
                page_number), many=True, context={"request": request})

            page_count = math.ceil(product_query.count()/int(page_size))



            main_banner = category_obj.mainbanner_set.all()
            main_banner_serializer = MainBannerSAerializer(main_banner,many=True,context={"request": request})
            other_banner = category_obj.banner_set.all()
            other_banner_serializer = BannerSAerializer(other_banner,many=True,context={"request": request})
            page_content= Content.objects.filter(category=category_obj).first()
            page_content_serializer = ContentSerializer(page_content)

            return Response({
                            'page_content':page_content_serializer.data,
                            'main_banner':main_banner_serializer.data,
                            'other_banner':other_banner_serializer.data,
                            'current_page': int(page_number),
                            'page_count': page_count,
                            "main_category":main_category_serilizer.data,
                            "sub_category":sub_categories_serilizer.data,
                            'product': product_serializer.data,
                            'brands': brand_query},
                            status=status.HTTP_200_OK)


# class ProductDetail(APIView):
#     def get(self, request, id):
#         # pomp_instance=Product.objects.filter(id=id).first()
#         product_instance = get_object_or_404(Product, id=id)
#         product_serilizer = productDetailSerializer(
#             product_instance, context={"request": request})
#         comments = Comment.objects.filter(product__id=id).order_by('-created_at')
#         comments_serializer = CommentsSerializer(comments, many=True)
#         questions = Question.objects.filter(product__id=id).order_by('-created_at')
#         questions_serializer = QuestionSerializer(questions, many=True)
#         similar_product=Product.objects.filter(price__lte=product_instance.price+1000000,price__gte=product_instance.price-1000000)
#         similar_product_serializer=AllProductSerializer(similar_product,context={"request": request},many=True)
#         avg = comments.aggregate(avg_keyfiyat_rate=Avg('kefiyat_rate'), avg_arzesh_rate=Avg(
#             'arzesh_rate'), avg_user_rate=(Avg('kefiyat_rate')+Avg('arzesh_rate'))/2)
#         return Response({'product': product_serilizer.data, 'comments': comments_serializer.data, 'questions': questions_serializer.data, 'avg_rate': avg,'similar_product':similar_product_serializer.data}, status=status.HTTP_200_OK)

class ProductDetail(APIView):
    def get(self, request, id):
        product_instance = get_object_or_404(Product, id=id)
        product_serilizer = productDetailSerializer(
            product_instance, context={"request": request})
        comments = Comment.objects.filter(product__id=id).order_by('-created_at')
        comments_serializer = CommentsSerializer(comments, many=True)
        questions = Question.objects.filter(product__id=id).order_by('-created_at')
        questions_serializer = QuestionSerializer(questions, many=True)

        # Retrieve similar products based on price and category
        similar_product = Product.objects.filter(
            price__lte=product_instance.price + 1000000,
            price__gte=product_instance.price - 1000000,
            category__in=product_instance.category.all()
        )
        similar_product_serializer = AllProductSerializer(
            similar_product, context={"request": request}, many=True)

        avg = comments.aggregate(
            avg_keyfiyat_rate=Avg('kefiyat_rate'),
            avg_arzesh_rate=Avg('arzesh_rate'),
            avg_user_rate=(Avg('kefiyat_rate') + Avg('arzesh_rate')) / 2
        )

        return Response({
            'product': product_serilizer.data,
            'comments': comments_serializer.data,
            'questions': questions_serializer.data,
            'avg_rate': avg,
            'similar_product': similar_product_serializer.data
        }, status=status.HTTP_200_OK)



# helping api for front
class ProductID(APIView):
    def get(self, request):
        ids = Product.objects.all().values_list('id', flat=True)[:30]
        srz = ProductIDSerializer(ids, many=True)
        return Response(srz.data, status=status.HTTP_200_OK)


# class AllProducts(APIView):
#     def get(self,request):
#         product_query=Product.objects.with_final_price()


#         category = self.request.query_params.get('category', None)
#         if category is not None:
#             product_query = product_query.filter(category__name=category)
#             brand_query = brand_query.filter(product__category__name=category)
#             # brand_query = brand_query.filter(product__in=product_query)

        # brand = self.request.query_params.getlist('brand[]')
        # if brand:
        #     product_query=product_query.filter(brand__name__in=brand)

        # min_price = self.request.query_params.get('min_price', None)
        # max_price = self.request.query_params.get('max_price', None)
        # if min_price and max_price:
        #     product_query=product_query.filter(final_price_Manager__gte=int(min_price),final_price_Manager__lte=int(max_price))

        # ordering = self.request.query_params.get('ordering', None)
        # if ordering is not None:
        #     if ordering=='asc':
        #         product_query = product_query.order_by('final_price_Manager')
        #     elif ordering=='des':
        #         product_query = product_query.order_by('-final_price_Manager')

        # product_serializer= AllProductSerializer(product_query,many=True)
        # brand_query =  product_query.values('brand__name').annotate(product_count=Count('brand'))
        # return Response({'product':product_serializer.data,'brand_count':brand_query},status=status.HTTP_200_OK)


class Pomps(APIView):

    def get(self, request):
        product_query = Product.objects.with_final_price().filter(
            category__name='پمپ').order_by('-created_at')

        brand_query_before = product_query.values('brand__name').annotate(
            product_count=Count('brand')).values('brand__id', 'brand__name', 'product_count')

        min_price = self.request.query_params.get('min_price', None)
        max_price = self.request.query_params.get('max_price', None)
        if min_price and max_price:
            product_query = product_query.filter(final_price_Manager__gte=int(
                min_price), final_price_Manager__lte=int(max_price))
            brand_query_before = product_query.values('brand__name').annotate(
                product_count=Count('brand')).values('brand__id', 'brand__name', 'product_count')

        brand_query = brand_query_before

        brand = self.request.query_params.getlist('brand[]')
        if brand:
            product_query = product_query.filter(brand__id__in=brand)
        else:
            brand_query = product_query.values('brand__name').annotate(
                product_count=Count('brand')).values('brand__id', 'brand__name', 'product_count')

        ordering = self.request.query_params.get('ordering', None)
        if ordering is not None:
            if ordering == 'price':
                product_query = product_query.order_by('final_price_Manager')
            elif ordering == '-price':
                product_query = product_query.order_by('-final_price_Manager')

        page_number = self.request.query_params.get('page', 1)
        # page_size = 20
        page_size = self.request.query_params.get('page_size', 20)

        paginator = Paginator(product_query, page_size)

        product_serializer = AllProductSerializer(paginator.page(
            page_number), many=True, context={"request": request})

        page_count = math.ceil(product_query.count()/int(page_size))

        return Response({'current_page': int(page_number), 'page_count': page_count, 'product': product_serializer.data, 'brands': brand_query}, status=status.HTTP_200_OK)


class HomePomps(APIView):
    def get(self, request):
        product_query = Product.objects.with_final_price().filter(
            category__name='پمپ اب خانگی').order_by('-created_at')

        brand_query_before = product_query.values('brand__id').annotate(
            product_count=Count('brand')).values('brand__id', 'brand__name', 'product_count')

        min_price = self.request.query_params.get('min_price', None)
        max_price = self.request.query_params.get('max_price', None)
        if min_price and max_price:
            product_query = product_query.filter(final_price_Manager__gte=int(
                min_price), final_price_Manager__lte=int(max_price))
            brand_query_before = product_query.values('brand__id').annotate(
                product_count=Count('brand')).values('brand__id', 'brand__name', 'product_count')

        brand_query = brand_query_before

        brand = self.request.query_params.getlist('brand[]')
        if brand:
            product_query = product_query.filter(brand__id__in=brand)
        else:
            brand_query = product_query.values('brand__id').annotate(product_count=Count(
                'brand')).values('brand__id', 'brand__name', 'product_count')

        ordering = self.request.query_params.get('ordering', None)
        if ordering is not None:
            if ordering == 'price':
                product_query = product_query.order_by('final_price_Manager')
            elif ordering == '-price':
                product_query = product_query.order_by('-final_price_Manager')

        page_number = self.request.query_params.get('page', 1)
        # page_size = 20
        page_size = self.request.query_params.get('page_size', 20)

        paginator = Paginator(product_query, page_size)

        product_serializer = AllProductSerializer(paginator.page(
            page_number), many=True, context={"request": request})

        page_count = math.ceil(product_query.count()/int(page_size))

        return Response({'current_page': int(page_number), 'page_count': page_count, 'product': product_serializer.data, 'brands': brand_query}, status=status.HTTP_200_OK)


class MohitiHomePomps(APIView):
    def get(self, request):
        product_query = Product.objects.with_final_price().filter(
            category__name='پمپ اب خانگی محیطی').order_by('-created_at')

        brand_query_before = product_query.values('brand__name').annotate(
            product_count=Count('brand')).values('brand__id', 'brand__name', 'product_count')

        min_price = self.request.query_params.get('min_price', None)
        max_price = self.request.query_params.get('max_price', None)
        if min_price and max_price:
            product_query = product_query.filter(final_price_Manager__gte=int(
                min_price), final_price_Manager__lte=int(max_price))
            brand_query_before = product_query.values('brand__name').annotate(
                product_count=Count('brand')).values('brand__id', 'brand__name', 'product_count')

        brand_query = brand_query_before

        brand = self.request.query_params.getlist('brand[]')
        if brand:
            product_query = product_query.filter(brand__id__in=brand)
        else:
            brand_query = product_query.values('brand__name').annotate(
                product_count=Count('brand')).values('brand__id', 'brand__name', 'product_count')

        ordering = self.request.query_params.get('ordering', None)
        if ordering is not None:
            if ordering == 'price':
                product_query = product_query.order_by('final_price_Manager')
            elif ordering == '-price':
                product_query = product_query.order_by('-final_price_Manager')

        page_number = self.request.query_params.get('page', 1)
        # page_size = 20
        page_size = self.request.query_params.get('page_size', 20)

        paginator = Paginator(product_query, page_size)

        product_serializer = AllProductSerializer(paginator.page(
            page_number), many=True, context={"request": request})

        page_count = math.ceil(product_query.count()/int(page_size))

        return Response({'current_page': int(page_number), 'page_count': page_count, 'product': product_serializer.data, 'brands': brand_query}, status=status.HTTP_200_OK)


class BoshghabiHomePomps(APIView):
    def get(self, request):
        product_query = Product.objects.with_final_price().filter(
            category__name='پمپ اب خانگی بشقابی').order_by('-created_at')

        brand_query_before = product_query.values('brand__name').annotate(
            product_count=Count('brand')).values('brand__id', 'brand__name', 'product_count')

        min_price = self.request.query_params.get('min_price', None)
        max_price = self.request.query_params.get('max_price', None)
        if min_price and max_price:
            product_query = product_query.filter(final_price_Manager__gte=int(
                min_price), final_price_Manager__lte=int(max_price))
            brand_query_before = product_query.values('brand__name').annotate(
                product_count=Count('brand')).values('brand__id', 'brand__name', 'product_count')

        brand_query = brand_query_before

        brand = self.request.query_params.getlist('brand[]')
        if brand:
            product_query = product_query.filter(brand__id__in=brand)
        else:
            brand_query = product_query.values('brand__name').annotate(
                product_count=Count('brand')).values('brand__id', 'brand__name', 'product_count')

        ordering = self.request.query_params.get('ordering', None)
        if ordering is not None:
            if ordering == 'price':
                product_query = product_query.order_by('final_price_Manager')
            elif ordering == '-price':
                product_query = product_query.order_by('-final_price_Manager')

        page_number = self.request.query_params.get('page', 1)
        # page_size = 20
        page_size = self.request.query_params.get('page_size', 20)

        paginator = Paginator(product_query, page_size)

        product_serializer = AllProductSerializer(paginator.page(
            page_number), many=True, context={"request": request})

        page_count = math.ceil(product_query.count()/int(page_size))

        return Response({'current_page': int(page_number), 'page_count': page_count, 'product': product_serializer.data, 'brands': brand_query}, status=status.HTTP_200_OK)


class JetiHomePomps(APIView):
    def get(self, request):
        product_query = Product.objects.with_final_price().filter(
            category__name='پمپ اب خانگی جتی').order_by('-created_at')

        brand_query_before = product_query.values('brand__name').annotate(
            product_count=Count('brand')).values('brand__id', 'brand__name', 'product_count')

        min_price = self.request.query_params.get('min_price', None)
        max_price = self.request.query_params.get('max_price', None)
        if min_price and max_price:
            product_query = product_query.filter(final_price_Manager__gte=int(
                min_price), final_price_Manager__lte=int(max_price))
            brand_query_before = product_query.values('brand__name').annotate(
                product_count=Count('brand')).values('brand__id', 'brand__name', 'product_count')

        brand_query = brand_query_before

        brand = self.request.query_params.getlist('brand[]')
        if brand:
            product_query = product_query.filter(brand__id__in=brand)
        else:
            brand_query = product_query.values('brand__name').annotate(
                product_count=Count('brand')).values('brand__id', 'brand__name', 'product_count')

        ordering = self.request.query_params.get('ordering', None)
        if ordering is not None:
            if ordering == 'price':
                product_query = product_query.order_by('final_price_Manager')
            elif ordering == '-price':
                product_query = product_query.order_by('-final_price_Manager')

        page_number = self.request.query_params.get('page', 1)
        # page_size = 20
        page_size = self.request.query_params.get('page_size', 20)

        paginator = Paginator(product_query, page_size)

        product_serializer = AllProductSerializer(paginator.page(
            page_number), many=True, context={"request": request})

        page_count = math.ceil(product_query.count()/int(page_size))

        return Response({'current_page': int(page_number), 'page_count': page_count, 'product': product_serializer.data, 'brands': brand_query}, status=status.HTTP_200_OK)


class DoParvaneHomePomps(APIView):
    def get(self, request):
        product_query = Product.objects.with_final_price().filter(
            category__name='پمپ اب خانگی دو پروانه').order_by('-created_at')

        brand_query_before = product_query.values('brand__name').annotate(
            product_count=Count('brand')).values('brand__id', 'brand__name', 'product_count')

        min_price = self.request.query_params.get('min_price', None)
        max_price = self.request.query_params.get('max_price', None)
        if min_price and max_price:
            product_query = product_query.filter(final_price_Manager__gte=int(
                min_price), final_price_Manager__lte=int(max_price))
            brand_query_before = product_query.values('brand__name').annotate(
                product_count=Count('brand')).values('brand__id', 'brand__name', 'product_count')

        brand_query = brand_query_before

        brand = self.request.query_params.getlist('brand[]')
        if brand:
            product_query = product_query.filter(brand__id__in=brand)
        else:
            brand_query = product_query.values('brand__name').annotate(
                product_count=Count('brand')).values('brand__id', 'brand__name', 'product_count')

        ordering = self.request.query_params.get('ordering', None)
        if ordering is not None:
            if ordering == 'price':
                product_query = product_query.order_by('final_price_Manager')
            elif ordering == '-price':
                product_query = product_query.order_by('-final_price_Manager')

        page_number = self.request.query_params.get('page', 1)
        # page_size = 20
        page_size = self.request.query_params.get('page_size', 20)

        paginator = Paginator(product_query, page_size)

        product_serializer = AllProductSerializer(paginator.page(
            page_number), many=True, context={"request": request})

        page_count = math.ceil(product_query.count()/int(page_size))

        return Response({'current_page': int(page_number), 'page_count': page_count, 'product': product_serializer.data, 'brands': brand_query}, status=status.HTTP_200_OK)
