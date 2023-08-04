from django.urls import include
from django.urls import path
from extention import views

urlpatterns = [
    path('home/',views.HomeApi.as_view()),
]
