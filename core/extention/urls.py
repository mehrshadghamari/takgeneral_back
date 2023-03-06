from django.urls import path,include
from extention import views


urlpatterns = [
    path('slider/',views.SliderApi.as_view()),

]