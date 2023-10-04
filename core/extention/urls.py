from django.urls import path
from extention import views

urlpatterns = [
    path('home/', views.HomeApi.as_view()),
    path('ads/', views.contentAPI.as_view()),
    path('blogs/', views.BlogsApi.as_view()),
    path('blog-detail/<slug:slug>/', views.BlogDetail.as_view()),
    path('redirects/' , views.RedirectView.as_view())
]
