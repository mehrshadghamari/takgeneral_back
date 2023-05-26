from account.models import MyUser
from django.db.models import F
from django.db.models import IntegerField
from django.db.models import Value
from product.models import Product
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Order
from .models import OrderItem
from .serializers import CartSerializer
from .serializers import OrderItemSerializer
from .serializers import OrderlistSerializer


class CartDetailsPreview(APIView):
    def post(self, request):
        cart_data = request.data.get('cartsData', None)
        if cart_data is None:
            return Response({'error': 'Invalid input data'}, status=status.HTTP_400_BAD_REQUEST)
        # elif not cart_data:
        #     return Response({'products': [], 'total_price': 0, 'total_final_price': 0, 'total_discount_price': 0, 'total_count': 0})

         # Filter out objects with count = 0 from the cart_data list
        # filtered_cart_data = [item for item in cart_data if item['count'] != 0]

        print('tttttttttttttttttttttttttttt')
        print(cart_data)
        user_id = request.user.id
        # user_id = 1
        # print(user_id)
        # user authentiicated
        if user_id is not None:
            print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
            user = MyUser.objects.get(id=user_id)
            # Get the user's unpaid order, if any
            order = Order.objects.filter(user=user, paid=False).first()

            if order is None:
                # Create a new order
                order = Order.objects.create(user=user)

            # Validate input data
            serializer = CartSerializer(data=cart_data, many=True)
            serializer.is_valid(raise_exception=True)
            cart_items = serializer.validated_data

            # Add cart items to the order or update the quantity if the product is already in the order
            for item in cart_items:
                product = Product.objects.get(id=item['id'])
                count = item['count']
                if count == 0:  # Check if count is zero
                    # Delete the OrderItem if it exists and count is zero
                    OrderItem.objects.filter(order=order, product=product).delete()
                else:
                    order_item, created = OrderItem.objects.get_or_create(
                        order=order, product=product)
                    if not created:
                        order_item.quantity = item['count']
                        order_item.save()
                    else:
                        order_item.quantity = item['count']
                        order_item.save()

            order_items = order.items.all()
            items = OrderItemSerializer(order_items, many=True)

            order_data = {
                'order_id': order.id,
                'paid': order.paid,
                'products': items.data,
                'total_price': order.total_price,
                'total_final_price': order.total_final_price,
                'total_discount_price': order.total_discount_price,
                'total_count': order.total_count,
            }
            return Response(order_data, status=status.HTTP_200_OK)

        # user not authentiicated
        else:
            if not cart_data:
                return Response({'products': [], 'total_price': 0, 'total_final_price': 0, 'total_discount_price': 0, 'total_count': 0})
            
            #  Filter out objects with count = 0 from the cart_data list
            filtered_cart_data = [item for item in cart_data if item['count'] != 0]

            print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
            serializer = CartSerializer(data=filtered_cart_data, many=True)
            serializer.is_valid(raise_exception=True)
            cart_items = serializer.validated_data

            # Calculate order details
            products = [Product.objects.with_final_price().filter(id=item['id']).annotate(
                quantity=Value(item['count'], IntegerField()),
                sum_final_price=F('final_price_Manager') *
                Value(item['count'], IntegerField()),
                sum_price=F('price') * Value(item['count'], IntegerField()),
                sum_discount_price=F('sum_price') - F('sum_final_price')
            ).first() for item in cart_items]

            total_price = sum([p.sum_price for p in products])
            total_final_price = sum([p.sum_final_price for p in products])
            total_discount_price = sum(
                [p.sum_discount_price for p in products])
            total_count = sum([p.quantity for p in products])

            # Serialize response data
            product_serializer = OrderlistSerializer(products, many=True)
            order_data = {
                'order_id': None,
                'paid': None,
                'products': product_serializer.data,
                'total_price': total_price,
                'total_final_price': total_final_price,
                'total_discount_price': total_discount_price,
                'total_count': total_count,
            }

            return Response(order_data, status=status.HTTP_200_OK)
