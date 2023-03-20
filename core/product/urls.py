from django.urls import path,include
from product import views


urlpatterns = [
    path('product-detail/<int:id>/',views.HomePompDetail.as_view()),
    
]