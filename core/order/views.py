from datetime import datetime

from account.models import MyUser
from django.db.models import F
from django.db.models import IntegerField
from django.db.models import Value
from django.shortcuts import get_object_or_404
from product.models import ProductVariant
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.helpers.zarinpal import ZarinPal
from core.settings import ZARINPAL_CONFIG

from .models import Order
from .models import OrderItem
from .serializers import CartSerializer
from .serializers import OrderItemSerializer
from .serializers import OrderlistSerializer
from .serializers import PaymentSerializer


class CartDetailsPreview(APIView):
    def post(self, request):
        cart_data = request.data.get("cartsData", None)
        if cart_data is None:
            return Response({"error": "Invalid input data"}, status=status.HTTP_400_BAD_REQUEST)

        user_id = request.user.id
        # user is authentiicated
        if user_id is not None:
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
                product = ProductVariant.objects.get(id=item["id"])
                count = item["count"]
                if count == 0:  # Check if count is zero
                    # Delete the OrderItem if it exists and count is zero
                    OrderItem.objects.filter(order=order, product=product).delete()
                else:
                    order_item, created = OrderItem.objects.get_or_create(order=order, product=product)
                    if not created:
                        order_item.quantity = item["count"]
                        order_item.save()
                    else:
                        order_item.quantity = item["count"]
                        order_item.save()

            order_items = order.items.all()
            items = OrderItemSerializer(order_items, many=True, context={"request": request})

            order_data = {
                "order_id": order.id,
                "paid": order.paid,
                "products": items.data,
                "total_price": order.total_price,
                "total_final_price": order.total_final_price,
                "total_discount_price": order.total_discount_price,
                "total_count": order.total_count,
            }

        # user is not authentiicated
        else:
            if not cart_data:
                return Response(
                    {
                        "products": [],
                        "total_price": 0,
                        "total_final_price": 0,
                        "total_discount_price": 0,
                        "total_count": 0,
                    }
                )

            #  Filter out objects with count = 0 from the cart_data list
            filtered_cart_data = [item for item in cart_data if item["count"] != 0]

            serializer = CartSerializer(data=filtered_cart_data, many=True)
            serializer.is_valid(raise_exception=True)
            cart_items = serializer.validated_data

            # Calculate order details
            products = [
                ProductVariant.objects.with_final_price()
                .filter(id=item["id"])
                .annotate(
                    quantity=Value(item["count"], IntegerField()),
                    sum_final_price=F("final_price_manager") * Value(item["count"], IntegerField()),
                    sum_price=F("price") * Value(item["count"], IntegerField()),
                    sum_discount_price=F("sum_price") - F("sum_final_price"),
                )
                .first()
                for item in cart_items
            ]

            total_price = int(sum([p.sum_price for p in products]))
            total_final_price = int(sum([p.sum_final_price for p in products]))
            total_discount_price = int(sum([p.sum_discount_price for p in products]))
            total_count = int(sum([p.quantity for p in products]))

            # Serialize response data
            product_serializer = OrderlistSerializer(products, many=True, context={"request": request})
            order_data = {
                "order_id": None,
                "paid": None,
                "products": product_serializer.data,
                "total_price": total_price,
                "total_final_price": total_final_price,
                "total_discount_price": total_discount_price,
                "total_count": total_count,
            }

        return Response(order_data, status=status.HTTP_200_OK)


# payment api


class Pay(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = self.request.user
        serializer = PaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order_data = serializer.validated_data
        order_object = get_object_or_404(Order, id=order_data["order_id"], paid=False)

        zp = ZarinPal(
            amount=order_object.total_final_price,  # toman
            detail=order_data.get("order_description")
            if order_data.get("order_description", None)
            else f" بابت خرید محصول از سایت تک جنرال",
            email=ZARINPAL_CONFIG["EMAIL"],
            phone_number=user.phone_number,
            callback=ZARINPAL_CONFIG["CALLBACK_URL"],
        )

        url, authority = zp.pay()

        order_object.authority = authority
        order_object.status = "PENDING"
        order_object.save()

        return Response({"payment_link": url}, status=status.HTTP_200_OK)


class VerfyPaymnet(APIView):
    def get(self, request):
        payment_status = request.query_params.get("Status")
        authority = request.query_params.get("Authority")
        order_object = Order.objects.filter(authority=authority, status="PENDING").first()
        if order_object:
            payment_status, ref_id, msg, card_pan_mask = ZarinPal.payment_validation(
                amount=order_object.total_final_price, authority=order_object.authority
            )
            if payment_status == "OK":
                order_object.paid = True
                order_object.Payment_ref_id = ref_id
                order_object.Payment_time = datetime.now()
                order_object.status = "PROCESSING"
                order_object.save()

        else:
            payment_status = "NOK"
            ref_id = 0

        if payment_status == "OK":
            return Response(
                {
                    "message": "Transaction success. RefID: " + str(ref_id),
                    "msg": msg,
                    "ref_id": ref_id,
                    "card_pan_mask": card_pan_mask,
                }
            )
            # return HttpResponseRedirect('http://127.0.0.1:8000/admin/order/order/')
        else:
            return Response({"message": "Transaction failed or canceled by user"})
            # return HttpResponseRedirect('https://yourdomain.com/failure-page/')
