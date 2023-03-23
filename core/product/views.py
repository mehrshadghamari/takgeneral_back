from django.shortcuts import render,get_object_or_404
from django.db.models import Count
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import Product
from .serializers import HomePompDetailSerializer,ProductIDSerializer,AllProductSerializer

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
    


class AllProducts(APIView):
    # filterset_fields = ['brand__name']
    # ordering_fields = []
    # search_fileds = [
        # 'name',      
        # 'category',        
        # 'brand',
    # ]
    def get(self,request):
        all_products = Product.objects.all()
        serializer = AllProductSerializer(all_products,many=True,context={"request": request})
        # Product.objects.aggregate(count_of_brands=Count('brand'))
        return Response(serializer.data,status=status.HTTP_200_OK)



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