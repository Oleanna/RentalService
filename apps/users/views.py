from apps.users.models import User
from apps.users.serializer import UserCreateSerializer, UserDetailSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from apps.users.serializer import EmailTokenObtainPairSerializer
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny


class UserRegisterAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = (AllowAny,)

class UserDetailAPIView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer

class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = EmailTokenObtainPairSerializer