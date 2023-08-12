from django.db.models import F
from django.db.models import Q
from django.shortcuts import render

from extention.models import Blog
from extention.models import Content

from extention.serializers import AllBlogSerializer
from extention.serializers import BlogSerializer
from extention.serializers import ContentSerializer
from product.models import Product
from product.serializers import AllProductSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView




class HomeApi(APIView):
    def get(self, request):
        special_offer_products = Product.objects.filter(special_offer=True)
        special_offer_serializer = AllProductSerializer(
            special_offer_products, many=True, context={"request": request})
        # amazing_offer_product=Product.objects.filter(discount__gte=20)
        amazing_offer_product = Product.objects.with_final_price().annotate(ekhtelaf=F(
            'price') - F('final_price_Manager')).filter(Q(ekhtelaf__gte=1000000) | Q(discount__gte=20))
        # amazing_offer_product=Product.objects.annotate(final_price=F('price')-(F('price')*F('discount')/100)).annotate(ekhtelaf=F('price') - F('final_price')).filter(ekhtelaf__gte=1000000)
        # amazing_offer_product=Product.objects.annotate(ekhtelaf=F('price') - F('final_price')).filter(ekhtelaf__gte=1000000)
        amazing_offer_serializer = AllProductSerializer(
            amazing_offer_product, many=True, context={"request": request})
        return Response({'special_offer_products': special_offer_serializer.data, 'amazing_offer_product': amazing_offer_serializer.data}, status=status.HTTP_200_OK)




class contentAPI(APIView):
    def get(self, request):
        advertisement = Content.objects.all()
        advertisement_serializer = ContentSerializer(
            advertisement, many=True,)
        return Response(advertisement_serializer.data, status=status.HTTP_200_OK)


class BlogsApi(APIView):
    def get(self, request):
        blogs = Blog.objects.all()
        blogs_serializer = AllBlogSerializer(
            blogs, many=True, context={"request": request})
        return Response(blogs_serializer.data, status=status.HTTP_200_OK)



class BlogDetail (APIView):
    def get(self, request,id):
        blog = Blog.objects.get(id=id)
        blog_serializer = BlogSerializer(
            blog, context={"request": request})
        return Response(blog_serializer.data, status=status.HTTP_200_OK)
