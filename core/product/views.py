from django.shortcuts import render,get_object_or_404
from django.db.models import Count,Q
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
# from rest_framework.filters import 
from rest_framework import generics
from .models import Product,ProductBrand
from .serializers import HomePompDetailSerializer,ProductIDSerializer,AllProductSerializer,productCountFromSpecificBrand

from rest_framework.pagination import LimitOffsetPagination
from django.core.paginator import Paginator
import math


class ProductDetail(APIView):
    def get(self,request,id):
        # pomp_instance=Product.objects.filter(id=id).first()
        pomp_instance=get_object_or_404(Product,id=id)
        serilizer=HomePompDetailSerializer(pomp_instance,context={"request": request})
        return Response(serilizer.data,status=status.HTTP_200_OK)
    

# helping api for front
class ProductID(APIView):
    def get(self,request):
        ids=Product.objects.all().values_list('id',flat=True)[:30]
        srz=ProductIDSerializer(ids,many=True)
        return Response(srz.data,status=status.HTTP_200_OK)




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
    
    def get(self,request):
        product_query=Product.objects.with_final_price().filter(category__name='پمپ').order_by('-created_at')

        brand_query_before =  product_query.values('brand__name').annotate(product_count=Count('brand')).values('brand__id','brand__name','product_count')


        min_price = self.request.query_params.get('min_price', None) 
        max_price = self.request.query_params.get('max_price', None)
        if min_price and max_price:
            product_query=product_query.filter(final_price_Manager__gte=int(min_price),final_price_Manager__lte=int(max_price)) 
            brand_query_before =  product_query.values('brand__name').annotate(product_count=Count('brand')).values('brand__id','brand__name','product_count')


        brand_query = brand_query_before

        brand = self.request.query_params.getlist('brand[]')
        if brand:
            product_query=product_query.filter(brand__id__in=brand)
        else:
            brand_query =  product_query.values('brand__name').annotate(product_count=Count('brand')).values('brand__id','brand__name','product_count')


        ordering = self.request.query_params.get('ordering', None)
        if ordering is not None:
            if ordering=='price':
                product_query = product_query.order_by('final_price_Manager')
            elif ordering=='-price':
                product_query = product_query.order_by('-final_price_Manager')

        page_number = self.request.query_params.get('page', 1)
        # page_size = 20
        page_size = self.request.query_params.get('page_size', 20)
        
        paginator = Paginator(product_query , page_size)

        product_serializer= AllProductSerializer(paginator.page(page_number),many=True,context={"request": request}) 



        page_count = math.ceil(product_query.count()/int(page_size))

        return Response({'current_page':int(page_number),'page_count':page_count,'product':product_serializer.data,'brands':brand_query},status=status.HTTP_200_OK)




class HomePomps(APIView):
    def get(self,request):
        product_query=Product.objects.with_final_price().filter(category__name='پمپ اب خانگی').order_by('-created_at')

        brand_query_before =  product_query.values('brand__id').annotate(product_count=Count('brand')).values('brand__id','brand__name','product_count')


        min_price = self.request.query_params.get('min_price', None) 
        max_price = self.request.query_params.get('max_price', None)
        if min_price and max_price:
            product_query=product_query.filter(final_price_Manager__gte=int(min_price),final_price_Manager__lte=int(max_price)) 
            brand_query_before =  product_query.values('brand__id').annotate(product_count=Count('brand')).values('brand__id','brand__name','product_count')


        brand_query = brand_query_before
        
        brand = self.request.query_params.getlist('brand[]')
        if brand:
            product_query=product_query.filter(brand__id__in=brand)
        else:
            brand_query =  product_query.values('brand__id').annotate(product_count=Count('brand')).values('brand__id','brand__name','product_count')


        ordering = self.request.query_params.get('ordering', None)
        if ordering is not None:
            if ordering=='price':
                product_query = product_query.order_by('final_price_Manager')
            elif ordering=='-price':
                product_query = product_query.order_by('-final_price_Manager')

        page_number = self.request.query_params.get('page', 1)
        # page_size = 20
        page_size = self.request.query_params.get('page_size', 20)
        
        paginator = Paginator(product_query , page_size)

        product_serializer= AllProductSerializer(paginator.page(page_number),many=True,context={"request": request}) 



        page_count = math.ceil(product_query.count()/int(page_size))

        return Response({'current_page':int(page_number),'page_count':page_count,'product':product_serializer.data,'brands':brand_query},status=status.HTTP_200_OK)






class MohitiHomePomps(APIView):
    def get(self,request):
        product_query=Product.objects.with_final_price().filter(category__name='پمپ اب خانگی محیطی').order_by('-created_at')

        brand_query_before =  product_query.values('brand__name').annotate(product_count=Count('brand')).values('brand__id','brand__name','product_count')


        min_price = self.request.query_params.get('min_price', None) 
        max_price = self.request.query_params.get('max_price', None)
        if min_price and max_price:
            product_query=product_query.filter(final_price_Manager__gte=int(min_price),final_price_Manager__lte=int(max_price)) 
            brand_query_before =  product_query.values('brand__name').annotate(product_count=Count('brand')).values('brand__id','brand__name','product_count')


        brand_query = brand_query_before
        
        brand = self.request.query_params.getlist('brand[]')
        if brand:
            product_query=product_query.filter(brand__id__in=brand)
        else:
            brand_query =  product_query.values('brand__name').annotate(product_count=Count('brand')).values('brand__id','brand__name','product_count')


        ordering = self.request.query_params.get('ordering', None)
        if ordering is not None:
            if ordering=='price':
                product_query = product_query.order_by('final_price_Manager')
            elif ordering=='-price':
                product_query = product_query.order_by('-final_price_Manager')

        page_number = self.request.query_params.get('page', 1)
        # page_size = 20
        page_size = self.request.query_params.get('page_size', 20)
        
        paginator = Paginator(product_query , page_size)

        product_serializer= AllProductSerializer(paginator.page(page_number),many=True,context={"request": request}) 



        page_count = math.ceil(product_query.count()/int(page_size))

        return Response({'current_page':int(page_number),'page_count':page_count,'product':product_serializer.data,'brands':brand_query},status=status.HTTP_200_OK)

    




class BoshghabiHomePomps(APIView):
    def get(self,request):
        product_query=Product.objects.with_final_price().filter(category__name='پمپ اب خانگی بشقابی').order_by('-created_at')

        brand_query_before =  product_query.values('brand__name').annotate(product_count=Count('brand')).values('brand__id','brand__name','product_count')


        min_price = self.request.query_params.get('min_price', None) 
        max_price = self.request.query_params.get('max_price', None)
        if min_price and max_price:
            product_query=product_query.filter(final_price_Manager__gte=int(min_price),final_price_Manager__lte=int(max_price)) 
            brand_query_before =  product_query.values('brand__name').annotate(product_count=Count('brand')).values('brand__id','brand__name','product_count')


        brand_query = brand_query_before
        
        brand = self.request.query_params.getlist('brand[]')
        if brand:
            product_query=product_query.filter(brand__id__in=brand)
        else:
            brand_query =  product_query.values('brand__name').annotate(product_count=Count('brand')).values('brand__id','brand__name','product_count')


        ordering = self.request.query_params.get('ordering', None)
        if ordering is not None:
            if ordering=='price':
                product_query = product_query.order_by('final_price_Manager')
            elif ordering=='-price':
                product_query = product_query.order_by('-final_price_Manager')

        page_number = self.request.query_params.get('page', 1)
        # page_size = 20
        page_size = self.request.query_params.get('page_size', 20)
        
        paginator = Paginator(product_query , page_size)

        product_serializer= AllProductSerializer(paginator.page(page_number),many=True,context={"request": request}) 



        page_count = math.ceil(product_query.count()/int(page_size))

        return Response({'current_page':int(page_number),'page_count':page_count,'product':product_serializer.data,'brands':brand_query},status=status.HTTP_200_OK)

    





class JetiHomePomps(APIView):
    def get(self,request):
        product_query=Product.objects.with_final_price().filter(category__name='پمپ اب خانگی جتی').order_by('-created_at')

        brand_query_before =  product_query.values('brand__name').annotate(product_count=Count('brand')).values('brand__id','brand__name','product_count')


        min_price = self.request.query_params.get('min_price', None) 
        max_price = self.request.query_params.get('max_price', None)
        if min_price and max_price:
            product_query=product_query.filter(final_price_Manager__gte=int(min_price),final_price_Manager__lte=int(max_price)) 
            brand_query_before =  product_query.values('brand__name').annotate(product_count=Count('brand')).values('brand__id','brand__name','product_count')


        brand_query = brand_query_before
        
        brand = self.request.query_params.getlist('brand[]')
        if brand:
            product_query=product_query.filter(brand__id__in=brand)
        else:
            brand_query =  product_query.values('brand__name').annotate(product_count=Count('brand')).values('brand__id','brand__name','product_count')


        ordering = self.request.query_params.get('ordering', None)
        if ordering is not None:
            if ordering=='price':
                product_query = product_query.order_by('final_price_Manager')
            elif ordering=='-price':
                product_query = product_query.order_by('-final_price_Manager')

        page_number = self.request.query_params.get('page', 1)
        # page_size = 20
        page_size = self.request.query_params.get('page_size', 20)
        
        paginator = Paginator(product_query , page_size)

        product_serializer= AllProductSerializer(paginator.page(page_number),many=True,context={"request": request}) 



        page_count = math.ceil(product_query.count()/int(page_size))

        return Response({'current_page':int(page_number),'page_count':page_count,'product':product_serializer.data,'brands':brand_query},status=status.HTTP_200_OK)

    




class DoParvaneHomePomps(APIView):
    def get(self,request):
        product_query=Product.objects.with_final_price().filter(category__name='پمپ اب خانگی دو پروانه').order_by('-created_at')

        brand_query_before =  product_query.values('brand__name').annotate(product_count=Count('brand')).values('brand__id','brand__name','product_count')


        min_price = self.request.query_params.get('min_price', None) 
        max_price = self.request.query_params.get('max_price', None)
        if min_price and max_price:
            product_query=product_query.filter(final_price_Manager__gte=int(min_price),final_price_Manager__lte=int(max_price)) 
            brand_query_before =  product_query.values('brand__name').annotate(product_count=Count('brand')).values('brand__id','brand__name','product_count')


        brand_query = brand_query_before
        
        brand = self.request.query_params.getlist('brand[]')
        if brand:
            product_query=product_query.filter(brand__id__in=brand)
        else:
            brand_query =  product_query.values('brand__name').annotate(product_count=Count('brand')).values('brand__id','brand__name','product_count')


        ordering = self.request.query_params.get('ordering', None)
        if ordering is not None:
            if ordering=='price':
                product_query = product_query.order_by('final_price_Manager')
            elif ordering=='-price':
                product_query = product_query.order_by('-final_price_Manager')

        page_number = self.request.query_params.get('page', 1)
        # page_size = 20
        page_size = self.request.query_params.get('page_size', 20)
        
        paginator = Paginator(product_query , page_size)

        product_serializer= AllProductSerializer(paginator.page(page_number),many=True,context={"request": request}) 



        page_count = math.ceil(product_query.count()/int(page_size))

        return Response({'current_page':int(page_number),'page_count':page_count,'product':product_serializer.data,'brands':brand_query},status=status.HTTP_200_OK)
