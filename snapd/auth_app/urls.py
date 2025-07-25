# accounts/urls.py
from django.urls import path
from .views import RequestOTPView, VerifyOTPView

urlpatterns = [
    path('request-otp/', RequestOTPView.as_view()),
    path('verify-otp/', VerifyOTPView.as_view()),
]
