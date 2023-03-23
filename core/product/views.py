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
        product_query=Product.objects.with_final_price()
        brand_query = ProductBrand.objects.annotate(product_count=Count('product'))

        category = self.request.query_params.get('category', None)
        if category is not None:
            product_query = product_query.filter(category__name=category)
            # brand_query = brand_query.filter(product__category__name=category)
            brand_query = brand_query.filter(product__in=product_query)

        brand = self.request.query_params.get('brand', None) 
        if brand is not None:
            product_query=product_query.filter(brand__name=brand)
            # brand_query = brand_query.filter(product__brand__name=brand)
            brand_query = brand_query.filter(product__in=product_query)

        min_price = self.request.query_params.get('min_price', None) 
        max_price = self.request.query_params.get('max_price', None)
        if min_price and max_price:
            product_query=product_query.filter(final_price_Manager__gte=int(min_price),final_price_Manager__lte=int(max_price)) 
            brand_query = brand_query.filter(product__in=product_query)

        # if category is not None:
            # count_of_product_brand = ProductBrand.objects.filter(product__category__name=category).annotate(product_count=Count('product'))
        # else:    
            # count_of_product_brand = ProductBrand.objects.annotate(product_count=Count('product'))
        product_serializer= AllProductSerializer(product_query,many=True)    
        count_of_product_brand_serilizer = productCountFromSpecificBrand(brand_query,many=True)
        return Response({'product':product_serializer.data,'The number of assignments of a brand':count_of_product_brand_serilizer.data},status=status.HTTP_200_OK)
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