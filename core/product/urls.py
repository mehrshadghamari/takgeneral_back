from django.urls import include
from django.urls import path
from product import views

urlpatterns = [
    path('all-categories/', views.AllCategoryList.as_view()),
    path('products/<int:cat_id>/',views.products.as_view()),
    path('brands/<int:brand_id>/',views.Brands.as_view()),
    path('product-detail/<int:id>/',views.ProductDetail.as_view()),

]
