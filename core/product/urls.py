from django.urls import path
from product import views

urlpatterns = [
    path('all-categories/', views.AllCategoryList.as_view()),
    path('products/<slug:cat_url>/', views.products.as_view()),
    path('brands/<slug:brand_url>/', views.Brands.as_view()),
    path('product-detail/<int:id>/', views.ProductDetail.as_view()),

]
