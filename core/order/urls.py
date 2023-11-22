from django.urls import path
from order import views

urlpatterns = [
    path("cart-detail/", views.CartDetailsPreview.as_view()),
    path("request-to-payment", views.Pay.as_view()),
    path("callback-payment", views.VerfyPaymnet.as_view()),
]
