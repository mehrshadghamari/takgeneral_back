from django.urls import path
from product_action import views


urlpatterns = [
    path('comment/',views.ProductComment.as_view()),
]