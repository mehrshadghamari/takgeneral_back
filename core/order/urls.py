from django.urls import path
from order import views



urlpatterns = [
    path('order-befor-login/',views.ShoworderlistBeforLogin.as_view()),
    
    ]