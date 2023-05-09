from django.urls import path
from . import views

urlpatterns = [
    path('user-register-or-login-send-otp/',views.UserRegisterOrLoginSendOTp.as_view()),
    path('user-verify-otp/',views.UserVerifyOTP.as_view()),
    path('logout/',views.LogoutView.as_view()),
    path('user-info/',views.UserAddInfo.as_view()),
    path('user-address/',views.UserAdress.as_view()),
    path('user-status/',views.UserStatus.as_view()),
]
