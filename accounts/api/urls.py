from django.urls import path
from .views import RegisterAPIView, LoginAPIView, UserRetrieveAPIView, UserUpdateAPIView

app_name = 'accounts'

urlpatterns = [
    path('register/', RegisterAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('user/', UserRetrieveAPIView.as_view()),
    path('user/update/', UserUpdateAPIView.as_view())
]


