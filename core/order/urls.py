from django.urls import path
from order import views



urlpatterns = [
    path('order-list/',views.ShowOrderListBeforeLogin.as_view()),
    
    ]