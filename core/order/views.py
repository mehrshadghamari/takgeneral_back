from django.shortcuts import render
from django.db.models import F,Value,FloatField
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from product.models import Product
from .serializers import OrderlistSerializer,CartSerializer



# class ShoworderlistBeforLogin(APIView):
#     def post(self,request):
#         datas=OrderInput(request.data,many=True)
#         # datas = self.request.data.get('cartsData',None)
#         # datas=[{'id':3,'count':3},{'id':2,'count':1}]
#         print(datas)
#         print(type(datas))
#         print('*********************')
#         l=[]
#         all_count=0
#         for data in datas:
#             print(data)
#             print(type(data))
#             all_count+=data['count']
#             p=Product.objects.with_final_price().filter(id=data['id']).annotate(quantity=Value(data['count'],FloatField()),sum_price = F('final_price_Manager') * Value(data['count'],FloatField()))
#             l.append(p.first())

            
        
#         serz=OrderlistSerializer(l,many=True)

#         return Response({'order_list':serz.data,'all_count':all_count},status=status.HTTP_200_OK)


# cart_data=[{'id':3,'count':3},{'id':2,'count':1}]

class ShowOrderListBeforeLogin(APIView):
    def post(self, request):
        cart_data = request.data.get('cartsData', None)
        if not cart_data:
            return Response({'error': 'Invalid input data'}, status=status.HTTP_400_BAD_REQUEST)

        # Validate input data
        serializer = CartSerializer(data=cart_data, many=True)
        serializer.is_valid(raise_exception=True)
        cart_items = serializer.validated_data

        # Calculate order details
        products = [Product.objects.with_final_price().filter(id=item['id']).annotate(
            quantity=Value(item['count'], FloatField()),
            sum_final_price = F('final_price_Manager') * Value(item['count'], FloatField()),
            sum_price = F('price') * Value(item['count'], FloatField()),
            sum_discount_price = F('sum_price') - F('sum_final_price')
        ).first() for item in cart_items]

        total_price = sum([p.sum_price for p in products])
        total_final_price = sum([p.sum_final_price for p in products])
        total_discount_price = sum([p.sum_discount_price for p in products])
        total_count = sum([p.quantity for p in products])

        # Serialize response data
        product_serializer = OrderlistSerializer(products, many=True)
        order_data = {
            'products': product_serializer.data,
            'total_price': total_price,
            'total_final_price': total_final_price,
            'total_discount':total_discount_price,
            'total_count': total_count,
        }

        return Response(order_data, status=status.HTTP_200_OK)
