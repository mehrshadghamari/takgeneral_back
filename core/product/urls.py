from django.urls import path,include
from product import views


urlpatterns = [
    path('product-detail/<int:id>/',views.ProductDetail.as_view()),
    path('id-of-products/',views.ProductID.as_view()),
    
]