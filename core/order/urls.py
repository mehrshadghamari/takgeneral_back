from django.urls import path
from order import views



urlpatterns = [
    path('cart-detail/',views.CartDetailsPreview.as_view()),
    
    ]