from django.urls import path,include
from product import views


urlpatterns = [
    path('HomePompDetail/<int:id>/',views.HomePompDetail.as_view()),
    
]