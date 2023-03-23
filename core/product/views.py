from django.shortcuts import render,get_object_or_404
from django.db.models import Count
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
# from rest_framework.filters import 
from rest_framework import generics
from .models import Product,ProductBrand
from .serializers import HomePompDetailSerializer,ProductIDSerializer,AllProductSerializer,productCountFromSpecificBrand

class ProductDetail(APIView):
    def get(self,request,id):
        # pomp_instance=Product.objects.filter(id=id).first()
        pomp_instance=get_object_or_404(Product,id=id)
        serilizer=HomePompDetailSerializer(pomp_instance,context={"request": request})
        return Response(serilizer.data,status=status.HTTP_200_OK)
    

# helping api for front
class ProductID(APIView):
    def get(self,request):
        ids=Product.objects.all()[:30]
        srz=ProductIDSerializer(ids,many=True)
        return Response(srz.data,status=status.HTTP_200_OK)




# class AllProducts(generics.ListAPIView):
    # queryset = Product.objects.all()
    # serializer_class = AllProductSerializer
    # filterset_fields = ['brand__name']
    # search_fields = [
    # 'name',      
    # 'category__name',        
    # 'brand__name',
    # ]
    




class AllPomps(generics.ListAPIView):
    serializer_class = AllProductSerializer
    filterset_fields = ['brand__name']
    search_fields = [
    'name',      
    'category__name',        
    'brand__name',
    ]

    def get_queryset(self):
        return Product.objects.filter(category__name='پمپ')        


class AllProducts(APIView):
    def get(self,request):
        category = self.request.query_params.get('category') 
        brand = self.request.query_params.get('brand') 
        min_price = self.request.query_params.get('min_price') 
        max_price = self.request.query_params.get('max_price') 

        count_of_product_brand = ProductBrand.objects.filter(product__category__name=category).annotate(product_count=Count('product'))
        count_of_product_brand_serilizer = productCountFromSpecificBrand(count_of_product_brand,many=True)
        return Response(count_of_product_brand_serilizer.data,status=status.HTTP_200_OK)
# class AllPomps(APIView):
#     filterset_fields = ['brand__name']
#     # ordering_fields = []
#     search_fileds = [
#         'name',      
#         'category',        
#         'brand',
#     ]
#     def get(self,request):
#         all_pomps = Product.objects.filter(category__name='پمپ')


# class allHomePomps(APIView):
#     def get(self,request):
#         all_home_pomps = Product.objects.filter(category__name='پمپ اب خانگی')
    








# from product.models import Product,ProductBrand
# Product.objects.aggregate(count_of_brands=Count('brand'))
# ProductBrand.objects.aggregate(c=Count('product'))
# ProductBrand.objects.annotate(num=Count('product__set')).values('name','num')