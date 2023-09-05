from django.urls import path
from extention import views

urlpatterns = [
    path('home/', views.HomeApi.as_view()),
    path('ads/', views.contentAPI.as_view()),
    path('blogs/', views.BlogsApi.as_view()),
    path('blog-detail/<int:id>/', views.BlogDetail.as_view()),
]
