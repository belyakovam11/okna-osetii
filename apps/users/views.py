from django.contrib.auth.models import User
from rest_framework import viewsets, generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from .serializers import (
    UserSerializer,
    RegisterSerializer,
    ChangePasswordSerializer,
)


class IsOwnerOrAdmin(permissions.BasePermission):
    """Разрешает доступ владельцу объекта или администратору."""

    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_staff:
            return True
        return obj == request.user


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Просмотр пользователей.
    - list/retrieve: только администратор.
    - me: текущий пользователь.
    - change_password: смена своего пароля.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

    # ─────────────────────────────────────────────────────────
    # GET /api/users/users/me/
    # Возвращает данные текущего пользователя.
    # ─────────────────────────────────────────────────────────
    @action(
        detail=False,
        methods=['get'],
        permission_classes=[permissions.IsAuthenticated],
        url_path='me',
    )
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # ─────────────────────────────────────────────────────────
    # POST /api/users/users/change_password/
    # Тело: { old_password, new_password }
    # ─────────────────────────────────────────────────────────
    @action(
        detail=False,
        methods=['post'],
        permission_classes=[permissions.IsAuthenticated],
        url_path='change-password',
    )
    def change_password(self, request):
        serializer = ChangePasswordSerializer(
            data=request.data,
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {'detail': 'Пароль успешно изменён.'},
            status=status.HTTP_200_OK,
        )

    # ─────────────────────────────────────────────────────────
    # POST /api/users/users/{id}/toggle_active/
    # Активация/деактивация пользователя (только админ).
    # ─────────────────────────────────────────────────────────
    @action(
        detail=True,
        methods=['post'],
        permission_classes=[permissions.IsAdminUser],
        url_path='toggle-active',
    )
    def toggle_active(self, request, pk=None):
        user = self.get_object()
        user.is_active = not user.is_active
        user.save(update_fields=['is_active'])
        return Response(
            {
                'id': user.id,
                'is_active': user.is_active,
                'detail': 'Пользователь активирован.' if user.is_active
                          else 'Пользователь деактивирован.',
            },
            status=status.HTTP_200_OK,
        )


class RegisterView(generics.CreateAPIView):
    """
    POST /api/users/register/
    Тело: { username, email, password, password2, first_name?, last_name? }
    Возвращает созданного пользователя и токен.
    """
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Создаём токен для авторизации
        token, _ = Token.objects.get_or_create(user=user)

        return Response(
            {
                'user': UserSerializer(user, context={'request': request}).data,
                'token': token.key,
                'detail': 'Регистрация прошла успешно.',
            },
            status=status.HTTP_201_CREATED,
        )


class ProfileView(generics.RetrieveUpdateAPIView):
    """
    GET/PUT/PATCH /api/users/profile/
    Просмотр и редактирование своего профиля.
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    parser_classes = [FormParser, MultiPartParser]


class LoginView(ObtainAuthToken):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code != status.HTTP_200_OK:
            return response
        user = Token.objects.get(key=response.data["token"]).user
        return Response(
            {
                "token": response.data["token"],
                "user": UserSerializer(user, context={"request": request}).data,
            },
            status=response.status_code,
        )

