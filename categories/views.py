from rest_framework import mixins
from rest_framework import viewsets, filters

from django.db.models import Avg

from django_filters.rest_framework import DjangoFilterBackend

from .models import Category, Genre, Title
from .filters import TitleFilter
from .serializers import CategorySerializer, GenreSerializer, TitleSerializer
from .permissions import HasAdminRoleOrRead


class DeleteViewSet(mixins.DestroyModelMixin,
                    mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    viewsets.GenericViewSet):
    pass


class CategoryViewSet(DeleteViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [HasAdminRoleOrRead, ]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'slug', ]
    lookup_field = 'slug'


class GenreViewSet(DeleteViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [HasAdminRoleOrRead, ]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'slug', ]
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(rating=Avg('reviews__score'))
    serializer_class = TitleSerializer
    permission_classes = [HasAdminRoleOrRead, ]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter
    filterset_fields = ['category', 'genre', 'name', 'year', ]
