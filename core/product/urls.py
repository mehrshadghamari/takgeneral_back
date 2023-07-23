from django.urls import include
from django.urls import path
from product import views

urlpatterns = [
    path('all-categories/', views.AllCategoryList.as_view(),),
    path('products/<int:cat_id>/', views.products.as_view()),
    path('brands/<int:brand_id>/', views.Brands.as_view()),
    path('product-detail/<int:id>/', views.ProductDetail.as_view()),
    path('id-of-products/', views.ProductID.as_view()),
    # path('all-products/',views.AllProducts.as_view()),
    path('pomps/', views.Pomps.as_view()),
    path('home-pomps/', views.HomePomps.as_view()),
    path('mohiti-home-pomps/', views.MohitiHomePomps.as_view()),
    path('boshghabi-home-pomps/', views.BoshghabiHomePomps.as_view()),
    path('jeti-home-pomps/', views.JetiHomePomps.as_view()),
    path('doparvane-home-pomps/', views.DoParvaneHomePomps.as_view()),

]
