from django.shortcuts import render
from django.db.models import F,Value,FloatField,IntegerField
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from product.models import Product
from .serializers import OrderlistSerializer,CartSerializer



# cart_data=[{'id':3,'count':3},{'id':2,'count':1}]


class CartDetailsPreview(APIView):
    def post(self, request):
        cart_data = request.data.get('cartsData', None)
        if cart_data is None:
            return Response({'error': 'Invalid input data'}, status=status.HTTP_400_BAD_REQUEST)
        elif not cart_data:
            return Response({'products': [], 'total_price': 0, 'total_final_price': 0, 'total_discount_price': 0, 'total_count': 0})
        
        # user = request.user.id
        # if user is not None:
        #     pass



        # Validate input data
        serializer = CartSerializer(data=cart_data, many=True)
        serializer.is_valid(raise_exception=True)
        cart_items = serializer.validated_data

        # Calculate order details
        products = [Product.objects.with_final_price().filter(id=item['id']).annotate(
            quantity=Value(item['count'], IntegerField()),
            sum_final_price = F('final_price_Manager') * Value(item['count'], IntegerField()),
            sum_price = F('price') * Value(item['count'], IntegerField()),
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
            'total_discount_price':total_discount_price,
            'total_count': total_count,
        }

        return Response(order_data, status=status.HTTP_200_OK)



# class CartDetailsPreview(APIView):
#     def post(self, request):
#         cart_data = request.data.get('cartsData', None)
#         if cart_data is None:
#             return Response({'error': 'Invalid input data'}, status=status.HTTP_400_BAD_REQUEST)
#         elif not cart_data:
#             return Response({'products': [], 'total_price': 0, 'total_final_price': 0, 'total_discount_price': 0, 'total_count': 0})

#         user = request.user
#         # Get the user's unpaid order, if any
#         order = Order.objects.filter(user=user, paid=False).first()

#         if order is None:
#             # Create a new order
#             order = Order.objects.create(user=user)

#         # Validate input data
#         serializer = CartSerializer(data=cart_data, many=True)
#         serializer.is_valid(raise_exception=True)
#         cart_items = serializer.validated_data

#         # Add cart items to the order or update the quantity if the product is already in the order
#         for item in cart_items:
#             product = Product.objects.get(id=item['id'])
#             order_item, created = OrderItem.objects.get_or_create(order=order, product=product)
#             if not created:
#                 order_item.quantity += item['count']
#                 order_item.save()
#             else:
#                 order_item.price = product.final_price_Manager
#                 order_item.quantity = item['count']
#                 order_item.save()

#         # Calculate order details
#         products = order.items.annotate(
#             quantity=F('quantity'),
#             sum_final_price=F('product__final_price_Manager') * F('quantity'),
#             sum_price=F('price') * F('quantity'),
#             sum_discount_price=F('sum_price') - F('sum_final_price')
#         )

#         total_price = products.aggregate(total_price=Sum('sum_price'))['total_price'] or 0
#         total_final_price = products.aggregate(total_final_price=Sum('sum_final_price'))['total_final_price'] or 0
#         total_discount_price = products.aggregate(total_discount_price=Sum('sum_discount_price'))['total_discount_price'] or 0
#         total_count = products.aggregate(total_count=Sum('quantity'))['total_count'] or 0

#         # Serialize response data
#         product_serializer = OrderlistSerializer(products, many=True)
#         order_data = {
#             'products': product_serializer.data,
#             'total_price': total_price,
#             'total_final_price': total_final_price,
#             'total_discount_price': total_discount_price,
#             'total_count': total_count,
#         }

#         return Response(order_data, status=status.HTTP_200_OK)