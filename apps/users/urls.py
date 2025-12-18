from django.urls import path

from apps.users.views import UserRegisterAPIView, UserDetailAPIView

urlpatterns = [
    path('<int:pk>/', UserDetailAPIView.as_view()),
    path('auth/register/', UserRegisterAPIView.as_view()),

]