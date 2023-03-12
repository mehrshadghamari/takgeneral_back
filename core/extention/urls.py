from django.urls import path,include
from extention import views


urlpatterns = [
    path('home/',views.HomeApi.as_view()),
    path('ads/',views.AdvertisementAPi.as_view()),
    

]