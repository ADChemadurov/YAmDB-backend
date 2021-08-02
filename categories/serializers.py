from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Category, Genre, Title


class CategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    slug = serializers.SlugField(
        validators=[UniqueValidator(queryset=Category.objects.all())]
    )

    class Meta:
        fields = ('name', 'slug', )
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    slug = serializers.SlugField(
        validators=[UniqueValidator(queryset=Genre.objects.all())]
    )

    class Meta:
        fields = ('name', 'slug', )
        model = Genre


class GenreField(serializers.SlugRelatedField):
    def to_representation(self, value):
        return GenreSerializer(value).data


class CategoryField(serializers.SlugRelatedField):
    def to_representation(self, value):
        return CategorySerializer(value).data


class TitleSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    year = serializers.IntegerField(required=False, allow_null=True)
    genre = GenreField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all(),
        required=False,
        allow_null=True
    )
    category = CategoryField(
        slug_field='slug',
        queryset=Category.objects.all(),
        required=False,
        allow_null=True
    )
    description = serializers.CharField(required=False, allow_null=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Title
