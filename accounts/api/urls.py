from django.urls import path
from .views import RegisterAPIView, LoginAPIView, UserRetrieveUpdateAPIView

app_name = 'accounts'

urlpatterns = [
    path('register/', RegisterAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('user/<str:username>/', UserRetrieveUpdateAPIView.as_view()),
]
