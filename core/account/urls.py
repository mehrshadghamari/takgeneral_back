from django.urls import path
from account import views

# from azbankgateways.urls import az_bank_gateways_urls


urlpatterns = [
    path('user-register-or-login-send-otp/',views.UserRegisterOrLoginSendOTp.as_view()),
    path('user-verify-otp/',views.UserVerifyOTP.as_view()),
    path('logout/',views.LogoutView.as_view()),
    path('user-info/',views.UserAddInfo.as_view()),

]
