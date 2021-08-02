from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, TitleViewSet, GenreViewSet

API_VERSION = 'v1'


router_v1 = DefaultRouter()
router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register('genres', GenreViewSet, basename='genres')
router_v1.register('titles', TitleViewSet, basename='titles')

urlpatterns = [
    path(f'{API_VERSION}/', include(router_v1.urls)),
]
