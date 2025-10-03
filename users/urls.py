from django.urls import path
from .views import CurrentUserView,SignupView,VerifySignupOTP,RequestPasswordReset,VerifyOTP, ResetPassword

urlpatterns = [
    path('me/', CurrentUserView.as_view(), name='current-user'),
    path('request-reset/', RequestPasswordReset.as_view(), name='request-reset'),
    path('verify-otp/', VerifyOTP.as_view(), name='verify-otp'),
    path('reset-password/', ResetPassword.as_view(), name='reset-password'),

    path('signup/', SignupView.as_view(), name='signup'),
    path('verify-signup/', VerifySignupOTP.as_view(), name='verify-signup'),
]
