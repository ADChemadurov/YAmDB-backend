from django.urls import path
from django.urls.conf import include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import AllUserViewSet, CurrentUserViewSet, get_token, send_email

v1_router = DefaultRouter()
v1_router.register(r'users', AllUserViewSet, basename='list_all_users')

urlpatterns = [
    path('v1/users/me/', CurrentUserViewSet.as_view(), name='current_user'),
    path('v1/', include(v1_router.urls)),
    path('v1/auth/email/', send_email, name='send_email'),
    path('v1/auth/token/', get_token, name='send_email'),
    path(
        'v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'
    ),
]
