from django.urls import path
from .views import RegisterAPIView, LoginAPIView, UserRetrieveUpdateAPIView, ChangePasswordView

app_name = 'accounts'

urlpatterns = [
    path('register/', RegisterAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('user/<int:id>/', UserRetrieveUpdateAPIView.as_view()),
    path('change-password/', ChangePasswordView.as_view()),
]
