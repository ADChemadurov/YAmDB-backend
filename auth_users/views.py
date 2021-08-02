from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import viewsets, generics, status
from rest_framework.decorators import api_view, permission_classes

from rest_framework_simplejwt.tokens import RefreshToken

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string

from .models import YamdbUser
from .permissions import HasAdminRole
from .serializers import ListUsersSerializer
from api_yamdb.settings import EMAIL_HOST


class CurrentUserViewSet(generics.RetrieveUpdateAPIView):
    """
    Отображает информацию о текущем авторизованном пользователе,
    а так же позволяет редактировать информацию учетной записи.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        current_user = get_object_or_404(
            YamdbUser, username=request.user.username
        )
        serializer = ListUsersSerializer(current_user)
        return Response(serializer.data)

    def patch(self, request):
        current_user = get_object_or_404(
            YamdbUser, username=request.user.username
        )
        serializer = ListUsersSerializer(
            current_user, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AllUserViewSet(viewsets.ModelViewSet):
    """
    Класс отображает всех пользователей,
    а так же позволяет получить информацию о каждом отдельном пользователе,
    создавать новых пользователей, редактировать информацию о нем
    и удалять учетные записи.
    """
    queryset = YamdbUser.objects.all()
    serializer_class = ListUsersSerializer
    permission_classes = [permissions.IsAuthenticated, HasAdminRole]
    http_method_names = ('get', 'post', 'patch', 'delete',)
    lookup_field = 'username'


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def send_email(request):
    """ Отправяет email с кодом подтверждения для получения JWT токена. """
    confirmation_code = get_random_string(length=20)
    user_email = request.data['email']
    user = get_object_or_404(YamdbUser, email=user_email)
    user.confirmation_code = confirmation_code
    user.save()
    send_mail(
        'Код подверждения от YaMBD API',
        ('Приветствуем! '
         'Вот ваш код подверждения: {}'.format(confirmation_code)),
        EMAIL_HOST,
        ['{}'.format(user_email)],
        fail_silently=False,
    )
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def get_token(request):
    """
    Возвращает сгенерированный токен для авторизации и код для обновления
    токена, принимая email адрес и код подтверждения.
    """
    user_email = request.data['email']
    user = get_object_or_404(YamdbUser, email=user_email)
    user_conf_code = user.confirmation_code
    request_conf_code = request.data['confirmation_code']
    if user_conf_code == request_conf_code:
        refresh = RefreshToken.for_user(user)
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        return Response(data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)
